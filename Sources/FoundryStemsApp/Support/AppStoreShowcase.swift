import Foundation

struct AppStoreShotDescription: Identifiable {
    let id = UUID()
    let title: String
    let description: String
}

enum AppStoreShowcase {
    static let iconPlaceholderDescription = """
    Circular forge sigil on charcoal stone (#141210), with an amber crucible rune (#E8A849) at center, \
    thin steel-gray ring, and subtle ember sparks in the lower-right arc.
    """

    static let shotDescriptions: [AppStoreShotDescription] = [
        AppStoreShotDescription(
            title: "Shot 1 — Billet Rack",
            description: "Show the split forge layout with billet rack, active anvil editor, and hearth gauge, emphasizing the dark forge palette and amber strike accents."
        ),
        AppStoreShotDescription(
            title: "Shot 2 — Ore Drop",
            description: "Capture drag-and-drop charging with highlighted ember overlay while multiple ore files are dropped into the hearth."
        ),
        AppStoreShotDescription(
            title: "Shot 3 — Quench Notes",
            description: "Focus on billet detail editing: alloy picker, role tuning, and quench notes field with metallurgy language."
        ),
        AppStoreShotDescription(
            title: "Shot 4 — Bloom Cast",
            description: "Show the inspector controls with cast manifest action and completion status line after export."
        ),
        AppStoreShotDescription(
            title: "Shot 5 — Forge Defaults",
            description: "Display settings pane with default alloy, auto-quench behavior, and sigil placeholder guidance."
        )
    ]
}
