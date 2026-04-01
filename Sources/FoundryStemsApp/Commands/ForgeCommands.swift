import SwiftUI

struct ForgeCommands: Commands {
    @ObservedObject var viewModel: ForgeViewModel

    var body: some Commands {
        CommandGroup(replacing: .newItem) {
            Button("New Hearth") {
                viewModel.startFreshHearth()
            }
            .keyboardShortcut("n", modifiers: [.command])
            .accessibilityLabel("New hearth")
        }

        CommandMenu("Forge") {
            Button("Add Billet") {
                viewModel.addBlankBillet()
            }
            .keyboardShortcut("n", modifiers: [.command, .shift])

            Button("Drop Billet") {
                viewModel.removeSelectedBillet()
            }
            .keyboardShortcut(.delete, modifiers: [])
            .disabled(!viewModel.canRemoveSelectedBillet)

            Divider()

            Button("Open Ledger") {
                viewModel.openLedgerPanel()
            }
            .keyboardShortcut("o", modifiers: [.command])

            Button("Stamp Ledger") {
                viewModel.saveLedger()
            }
            .keyboardShortcut("s", modifiers: [.command])

            Button("Cast Bloom Manifest") {
                viewModel.exportBloomManifest()
            }
            .keyboardShortcut("e", modifiers: [.command, .shift])
        }
    }
}
