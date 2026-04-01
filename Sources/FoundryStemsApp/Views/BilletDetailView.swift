import SwiftUI

struct BilletDetailView: View {
    @ObservedObject var viewModel: ForgeViewModel

    var body: some View {
        Group {
            if let selectedBilletIndex = viewModel.selectedBilletIndex {
                let billet = $viewModel.session.billets[selectedBilletIndex]

                Form {
                    Section("Billet Core") {
                        TextField("Billet name", text: billet.billetName)
                            .accessibilityLabel("Billet name")

                        Picker("Alloy", selection: billet.alloy) {
                            ForEach(StemAlloy.allCases) { alloy in
                                Text(alloy.rawValue).tag(alloy)
                            }
                        }
                        .accessibilityLabel("Billet alloy")

                        Picker("Role", selection: billet.role) {
                            ForEach(StemRole.allCases) { role in
                                Text(role.rawValue).tag(role)
                            }
                        }
                        .accessibilityLabel("Billet role")
                    }

                    Section("Heat") {
                        Slider(value: heatBinding(for: selectedBilletIndex), in: 0 ... 100, step: 1)
                            .tint(Color.forgeAmber)
                            .accessibilityLabel("Billet heat")
                        Text("\(viewModel.session.billets[selectedBilletIndex].heat)% heat")
                            .font(.footnote.weight(.semibold))
                            .foregroundStyle(Color.forgeAmber)
                    }

                    Section("Ore Link") {
                        Text(viewModel.session.billets[selectedBilletIndex].sourcePath ?? "No ore file linked.")
                            .font(.callout)
                            .foregroundStyle(Color.forgeSmoke)
                            .textSelection(.enabled)
                            .accessibilityLabel("Ore link")
                    }

                    Section("Quench Notes") {
                        TextEditor(text: billet.quenchNotes)
                            .font(.body)
                            .frame(minHeight: 180)
                            .accessibilityLabel("Quench notes")
                    }
                }
                .scrollContentBackground(.hidden)
                .background(Color.forgeCharcoal)
                .onChange(of: viewModel.session.billets[selectedBilletIndex]) { _ in
                    viewModel.temperedFromWorkbench()
                }
            } else {
                ForgeEmptyView(
                    title: "No Billet on Anvil",
                    subtitle: "Select a billet from the rack, or drop ore files to charge this heat."
                )
            }
        }
        .padding(12)
        .background(Color.forgeCharcoal)
    }

    private func heatBinding(for index: Int) -> Binding<Double> {
        Binding<Double>(
            get: {
                Double(viewModel.session.billets[index].heat)
            },
            set: { newValue in
                viewModel.session.billets[index].heat = Int(newValue.rounded())
            }
        )
    }
}
