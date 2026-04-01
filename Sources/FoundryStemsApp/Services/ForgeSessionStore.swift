import Foundation

enum ForgeStoreFault: LocalizedError {
    case decodeFailure
    case encodeFailure

    var errorDescription: String? {
        switch self {
        case .decodeFailure:
            return "Ledger could not be read from the ingot marks."
        case .encodeFailure:
            return "Ledger could not be stamped to disk."
        }
    }
}

final class ForgeSessionStore {
    private let fileManager: FileManager
    private let encoder: JSONEncoder
    private let decoder: JSONDecoder
    private let autosaveURL: URL

    private(set) var activeSessionURL: URL?

    init(fileManager: FileManager = .default, storageRootURL: URL? = nil) {
        self.fileManager = fileManager

        encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        encoder.dateEncodingStrategy = .iso8601

        decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601

        let rootURL: URL
        if let storageRootURL {
            rootURL = storageRootURL
        } else {
            let appSupport = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first
                ?? fileManager.homeDirectoryForCurrentUser
            rootURL = appSupport.appendingPathComponent("FoundryStems/ForgeCache", isDirectory: true)
        }

        if !fileManager.fileExists(atPath: rootURL.path) {
            try? fileManager.createDirectory(at: rootURL, withIntermediateDirectories: true)
        }

        autosaveURL = rootURL.appendingPathComponent("autosave.forgeledger")
    }

    func loadAutosave() throws -> ForgeSession? {
        guard fileManager.fileExists(atPath: autosaveURL.path) else {
            return nil
        }
        let data = try Data(contentsOf: autosaveURL)
        var session = try decodeSession(from: data)
        session.normalize()
        return session
    }

    func loadSession(from url: URL) throws -> ForgeSession {
        let data = try readData(from: url)
        var session = try decodeSession(from: data)
        session.normalize()
        activeSessionURL = url
        return session
    }

    func saveSession(_ session: ForgeSession, to url: URL) throws {
        var session = session
        session.normalize()
        let data = try encodeSession(session)
        try writeData(data, to: url)
        activeSessionURL = url
        try autosave(session)
    }

    func autosave(_ session: ForgeSession) throws {
        var session = session
        session.normalize()
        let data = try encodeSession(session)
        try writeData(data, to: autosaveURL)
    }

    func clearAutosave() throws {
        guard fileManager.fileExists(atPath: autosaveURL.path) else {
            return
        }
        try fileManager.removeItem(at: autosaveURL)
    }

    func exportBloomManifest(for session: ForgeSession, to url: URL) throws {
        var session = session
        session.normalize()

        let manifest = BloomManifest(
            hearthTitle: session.hearthTitle,
            exportedAt: Date(),
            billetCount: session.billets.count,
            totalHeat: session.totalHeat,
            averageHeat: session.averageHeat,
            billets: session.billets.map { billet in
                BloomManifestBillet(
                    billetName: billet.billetName,
                    alloy: billet.alloy,
                    role: billet.role,
                    heat: billet.heat,
                    sourcePath: billet.sourcePath
                )
            }
        )

        let data = try encoder.encode(manifest)
        try writeData(data, to: url)
    }

    private func decodeSession(from data: Data) throws -> ForgeSession {
        do {
            return try decoder.decode(ForgeSession.self, from: data)
        } catch {
            throw ForgeStoreFault.decodeFailure
        }
    }

    private func encodeSession(_ session: ForgeSession) throws -> Data {
        do {
            return try encoder.encode(session)
        } catch {
            throw ForgeStoreFault.encodeFailure
        }
    }

    private func readData(from url: URL) throws -> Data {
        let shouldStopAccess = url.startAccessingSecurityScopedResource()
        defer {
            if shouldStopAccess {
                url.stopAccessingSecurityScopedResource()
            }
        }
        return try Data(contentsOf: url)
    }

    private func writeData(_ data: Data, to url: URL) throws {
        let shouldStopAccess = url.startAccessingSecurityScopedResource()
        defer {
            if shouldStopAccess {
                url.stopAccessingSecurityScopedResource()
            }
        }
        try data.write(to: url, options: .atomic)
    }
}
