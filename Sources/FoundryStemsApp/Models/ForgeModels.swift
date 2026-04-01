import Foundation

enum StemAlloy: String, Codable, CaseIterable, Identifiable {
    case brass = "Brass Weave"
    case iron = "Iron Grain"
    case steel = "Steel Spine"
    case copper = "Copper Mist"

    var id: String { rawValue }
}

enum StemRole: String, Codable, CaseIterable, Identifiable {
    case pulse = "Pulse Billet"
    case lead = "Lead Billet"
    case atmosphere = "Atmos Billet"
    case spark = "Spark Billet"

    var id: String { rawValue }
}

struct StemBillet: Identifiable, Codable, Hashable {
    var id: UUID
    var billetName: String
    var alloy: StemAlloy
    var role: StemRole
    var heat: Int
    var sourcePath: String?
    var quenchNotes: String
    var chargedAt: Date

    init(
        id: UUID = UUID(),
        billetName: String,
        alloy: StemAlloy,
        role: StemRole,
        heat: Int,
        sourcePath: String?,
        quenchNotes: String,
        chargedAt: Date = Date()
    ) {
        self.id = id
        self.billetName = billetName
        self.alloy = alloy
        self.role = role
        self.heat = min(max(heat, 0), 100)
        self.sourcePath = sourcePath
        self.quenchNotes = quenchNotes
        self.chargedAt = chargedAt
    }

    mutating func clampHeat() {
        heat = min(max(heat, 0), 100)
    }
}

struct ForgeSession: Identifiable, Codable {
    var id: UUID
    var hearthTitle: String
    var billets: [StemBillet]
    var forgedAt: Date
    var lastTemperedAt: Date?

    init(
        id: UUID = UUID(),
        hearthTitle: String,
        billets: [StemBillet],
        forgedAt: Date = Date(),
        lastTemperedAt: Date? = nil
    ) {
        self.id = id
        self.hearthTitle = hearthTitle
        self.billets = billets
        self.forgedAt = forgedAt
        self.lastTemperedAt = lastTemperedAt
    }

    mutating func normalize() {
        billets = billets.map { billet in
            var billet = billet
            billet.clampHeat()
            return billet
        }
    }

    var totalHeat: Int {
        billets.reduce(0) { $0 + $1.heat }
    }

    var averageHeat: Int {
        guard !billets.isEmpty else { return 0 }
        return totalHeat / billets.count
    }
}

struct BloomManifest: Codable {
    let hearthTitle: String
    let exportedAt: Date
    let billetCount: Int
    let totalHeat: Int
    let averageHeat: Int
    let billets: [BloomManifestBillet]
}

struct BloomManifestBillet: Codable {
    let billetName: String
    let alloy: StemAlloy
    let role: StemRole
    let heat: Int
    let sourcePath: String?
}
