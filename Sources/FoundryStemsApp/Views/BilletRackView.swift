import SwiftUI

struct BilletRackView: View {
    @ObservedObject var viewModel: ForgeViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Billet Rack")
                .font(.headline)
                .foregroundStyle(Color.forgeAmber)

            TextField("Hearth title", text: $viewModel.session.hearthTitle)
                .textFieldStyle(.roundedBorder)
                .onChange(of: viewModel.session.hearthTitle) { _ in
                    viewModel.temperedFromWorkbench()
                }
                .accessibilityLabel("Hearth title")

            if viewModel.session.billets.isEmpty {
                ForgeEmptyView(
                    title: "Rack is Cold",
                    subtitle: "Drop ore files or strike the add billet control to begin this heat."
                )
            } else {
                List(selection: $viewModel.selectedBilletID) {
                    ForEach(viewModel.session.billets) { billet in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(billet.billetName)
                                .font(.body.weight(.semibold))
                                .foregroundStyle(.primary)
                            Text("\(billet.role.rawValue) • \(billet.heat)% heat")
                                .font(.caption)
                                .foregroundStyle(Color.forgeSmoke)
                        }
                        .padding(.vertical, 4)
                        .tag(billet.id)
                        .accessibilityElement(children: .combine)
                        .accessibilityLabel("\(billet.billetName), \(billet.role.rawValue), \(billet.heat) percent heat")
                    }
                }
                .scrollContentBackground(.hidden)
                .background(Color.clear)
            }

            HStack {
                Button {
                    viewModel.addBlankBillet()
                } label: {
                    Label("Add Billet", systemImage: "plus")
                }
                .keyboardShortcut("n", modifiers: [.command, .shift])
                .accessibilityLabel("Add billet")

                Button {
                    viewModel.removeSelectedBillet()
                } label: {
                    Label("Drop Billet", systemImage: "trash")
                }
                .disabled(!viewModel.canRemoveSelectedBillet)
                .accessibilityLabel("Drop selected billet")
            }
            .buttonStyle(.bordered)
        }
        .padding(14)
        .background(Color.forgePanel.opacity(0.45))
    }
}
