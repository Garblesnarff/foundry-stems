import AppKit
import Combine
import Foundation
import UniformTypeIdentifiers

@MainActor
final class ForgeViewModel: ObservableObject {
    @Published var session: ForgeSession
    @Published var selectedBilletID: StemBillet.ID?
    @Published var forgeFault: String?
    @Published var statusLine: String?
    @Published var isDropTargeted = false

    private let store: ForgeSessionStore
    private let defaults = UserDefaults.standard
    private let ledgerType = UTType(filenameExtension: "forgeledger") ?? .json
    private let manifestType = UTType(filenameExtension: "bloommanifest") ?? .json

    init(store: ForgeSessionStore) {
        self.store = store
        self.session = ForgeSession(
            hearthTitle: "First Heat",
            billets: []
        )

        if shouldCacheLastHearth(), let autosaved = try? store.loadAutosave() {
            session = autosaved
            selectedBilletID = autosaved.billets.first?.id
            statusLine = "Recovered a warm ledger from the ash bin."
        }
    }

    var selectedBilletIndex: Int? {
        guard let selectedBilletID else { return nil }
        return session.billets.firstIndex(where: { $0.id == selectedBilletID })
    }

    var canRemoveSelectedBillet: Bool {
        selectedBilletIndex != nil
    }

    func startFreshHearth() {
        session = ForgeSession(
            hearthTitle: "Fresh Heat",
            billets: []
        )
        selectedBilletID = nil

        if !shouldCacheLastHearth() {
            try? store.clearAutosave()
        }

        quench("Hearth raked clean for the next pour.")
    }

    func addBlankBillet() {
        let billet = StemBillet(
            billetName: "Billet \(session.billets.count + 1)",
            alloy: preferredAlloy(),
            role: .pulse,
            heat: 62,
            sourcePath: nil,
            quenchNotes: "Awaiting hammer marks."
        )
        session.billets.append(billet)
        selectedBilletID = billet.id
        quench("A fresh billet was set on the anvil.")
    }

    func removeSelectedBillet() {
        guard let selectedBilletIndex else { return }
        let removedName = session.billets[selectedBilletIndex].billetName
        session.billets.remove(at: selectedBilletIndex)
        selectedBilletID = session.billets.first?.id
        quench("\(removedName) was returned to the slag bin.")
    }

    func ingestDroppedFiles(_ urls: [URL]) {
        ingestFileURLs(urls)
    }

    func ingestFileURLs(_ urls: [URL]) {
        guard !urls.isEmpty else { return }
        let billets = urls.map { url in
            StemBillet(
                billetName: url.deletingPathExtension().lastPathComponent,
                alloy: preferredAlloy(),
                role: role(for: url.lastPathComponent),
                heat: 70,
                sourcePath: url.path,
                quenchNotes: "Forged from ore file: \(url.lastPathComponent)"
            )
        }
        session.billets.append(contentsOf: billets)
        selectedBilletID = billets.last?.id
        quench("\(billets.count) ore files were charged into the hearth.")
    }

    func temperedFromWorkbench() {
        quench(nil)
    }

    func openLedgerPanel() {
        let panel = NSOpenPanel()
        panel.message = "Open a forged ledger"
        panel.allowedContentTypes = [ledgerType, .json]
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        panel.prompt = "Open Ledger"

        guard panel.runModal() == .OK, let url = panel.url else {
            return
        }

        do {
            let loaded = try store.loadSession(from: url)
            session = loaded
            selectedBilletID = loaded.billets.first?.id
            statusLine = "Ledger reopened from cooled iron."
            forgeFault = nil
        } catch {
            registerFault(error, prefix: "Failed to reopen ledger")
        }
    }

    func saveLedger() {
        if let activeSessionURL = store.activeSessionURL {
            persistSession(to: activeSessionURL, message: "Ledger tempered to disk.")
            return
        }
        saveLedgerAs()
    }

    func saveLedgerAs() {
        let panel = NSSavePanel()
        panel.message = "Stamp this ledger to disk"
        panel.allowedContentTypes = [ledgerType, .json]
        panel.nameFieldStringValue = defaultLedgerName()
        panel.prompt = "Stamp Ledger"

        guard panel.runModal() == .OK, let selectedURL = panel.url else {
            return
        }

        let targetURL = normalizedURL(selectedURL, ext: "forgeledger")
        persistSession(to: targetURL, message: "Ledger stamped to \(targetURL.lastPathComponent).")
    }

    func exportBloomManifest() {
        let panel = NSSavePanel()
        panel.message = "Cast a bloom manifest for this heat"
        panel.allowedContentTypes = [manifestType, .json]
        panel.nameFieldStringValue = defaultManifestName()
        panel.prompt = "Cast Manifest"

        guard panel.runModal() == .OK, let selectedURL = panel.url else {
            return
        }

        let targetURL = normalizedURL(selectedURL, ext: "bloommanifest")
        do {
            try store.exportBloomManifest(for: session, to: targetURL)
            statusLine = "Bloom manifest cast as \(targetURL.lastPathComponent)."
            forgeFault = nil
        } catch {
            registerFault(error, prefix: "Manifest casting failed")
        }
    }

    func clearFault() {
        forgeFault = nil
    }

    private func persistSession(to url: URL, message: String) {
        do {
            try store.saveSession(session, to: url)
            statusLine = message
            forgeFault = nil
        } catch {
            registerFault(error, prefix: "Ledger stamp failed")
        }
    }

    private func quench(_ line: String?) {
        session.lastTemperedAt = Date()

        guard shouldCacheLastHearth() else {
            if let line {
                statusLine = line
            }
            return
        }

        if shouldAutoQuench() {
            do {
                try store.autosave(session)
            } catch {
                registerFault(error, prefix: "Auto-quench failed")
                return
            }
        }

        if let line {
            statusLine = line
        }
    }

    private func shouldAutoQuench() -> Bool {
        if defaults.object(forKey: "autoQuenchEnabled") == nil {
            return true
        }
        return defaults.bool(forKey: "autoQuenchEnabled")
    }

    private func shouldCacheLastHearth() -> Bool {
        if defaults.object(forKey: "cacheLastHearth") == nil {
            return true
        }
        return defaults.bool(forKey: "cacheLastHearth")
    }

    private func preferredAlloy() -> StemAlloy {
        guard
            let raw = defaults.string(forKey: "defaultAlloy"),
            let alloy = StemAlloy(rawValue: raw)
        else {
            return .steel
        }
        return alloy
    }

    private func role(for filename: String) -> StemRole {
        let lowered = filename.lowercased()
        if lowered.contains("lead") {
            return .lead
        }
        if lowered.contains("fx") || lowered.contains("spark") {
            return .spark
        }
        if lowered.contains("pad") || lowered.contains("atmo") {
            return .atmosphere
        }
        return .pulse
    }

    private func registerFault(_ error: Error, prefix: String) {
        forgeFault = "\(prefix): \(error.localizedDescription)"
    }

    private func defaultLedgerName() -> String {
        "\(session.hearthTitle.replacingOccurrences(of: " ", with: "_").lowercased()).forgeledger"
    }

    private func defaultManifestName() -> String {
        "\(session.hearthTitle.replacingOccurrences(of: " ", with: "_").lowercased()).bloommanifest"
    }

    private func normalizedURL(_ url: URL, ext: String) -> URL {
        if url.pathExtension.isEmpty {
            return url.appendingPathExtension(ext)
        }
        if url.pathExtension == ext {
            return url
        }
        return url.deletingPathExtension().appendingPathExtension(ext)
    }
}
