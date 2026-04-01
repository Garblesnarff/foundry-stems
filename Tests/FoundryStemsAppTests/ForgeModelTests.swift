import XCTest
@testable import FoundryStemsApp

final class ForgeModelTests: XCTestCase {
    func testHeatClampsToSafeForgeRange() {
        var billet = StemBillet(
            billetName: "Overheated Core",
            alloy: .iron,
            role: .pulse,
            heat: 188,
            sourcePath: nil,
            quenchNotes: "Test"
        )

        XCTAssertEqual(billet.heat, 100)

        billet.heat = -30
        billet.clampHeat()
        XCTAssertEqual(billet.heat, 0)
    }
}
