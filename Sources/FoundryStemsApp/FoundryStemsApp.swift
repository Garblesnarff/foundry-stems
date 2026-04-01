import AppKit
import SwiftUI

@main
struct FoundryStemsApp: App {
    @StateObject private var viewModel = ForgeViewModel(store: ForgeSessionStore())

    init() {
        NSApp?.appearance = NSAppearance(named: .darkAqua)
    }

    var body: some Scene {
        WindowGroup("Foundry Stems") {
            ForgeWorkbenchView(viewModel: viewModel)
                .preferredColorScheme(.dark)
                .frame(minWidth: 1080, minHeight: 680)
        }
        .commands {
            ForgeCommands(viewModel: viewModel)
        }

        Settings {
            ForgeSettingsView()
                .preferredColorScheme(.dark)
                .padding(20)
                .frame(width: 560, height: 560)
        }
    }
}
