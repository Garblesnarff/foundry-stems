import Foundation
import XCTest
@testable import FoundryStemsApp

final class ForgeSessionStoreTests: XCTestCase {
    func testLedgerRoundTripAndManifestCast() throws {
        let fileManager = FileManager.default
        let tempRoot = fileManager.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
        try fileManager.createDirectory(at: tempRoot, withIntermediateDirectories: true)

        let store = ForgeSessionStore(fileManager: fileManager, storageRootURL: tempRoot)
        let session = ForgeSession(
            hearthTitle: "Night Heat",
            billets: [
                StemBillet(
                    billetName: "Pulse Core",
                    alloy: .steel,
                    role: .pulse,
                    heat: 70,
                    sourcePath: "/tmp/pulse.wav",
                    quenchNotes: "steady"
                ),
                StemBillet(
                    billetName: "Lead Shard",
                    alloy: .copper,
                    role: .lead,
                    heat: 80,
                    sourcePath: "/tmp/lead.wav",
                    quenchNotes: "bright"
                )
            ]
        )

        let ledgerURL = tempRoot.appendingPathComponent("night_heat.forgeledger")
        try store.saveSession(session, to: ledgerURL)
        let loaded = try store.loadSession(from: ledgerURL)
        XCTAssertEqual(loaded.hearthTitle, "Night Heat")
        XCTAssertEqual(loaded.billets.count, 2)

        let manifestURL = tempRoot.appendingPathComponent("night_heat.bloommanifest")
        try store.exportBloomManifest(for: loaded, to: manifestURL)
        let manifestData = try Data(contentsOf: manifestURL)
        let manifest = try JSONDecoder().decode(BloomManifest.self, from: manifestData)
        XCTAssertEqual(manifest.billetCount, 2)
        XCTAssertEqual(manifest.totalHeat, 150)
        XCTAssertEqual(manifest.averageHeat, 75)
    }
}
