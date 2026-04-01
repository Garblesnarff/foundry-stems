import SwiftUI

struct ForgeInspectorView: View {
    @ObservedObject var viewModel: ForgeViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Hearth Gauge")
                .font(.headline)
                .foregroundStyle(Color.forgeAmber)

            VStack(alignment: .leading, spacing: 8) {
                gaugeRow(label: "Billets", value: "\(viewModel.session.billets.count)")
                gaugeRow(label: "Total Heat", value: "\(viewModel.session.totalHeat)")
                gaugeRow(label: "Average Heat", value: "\(viewModel.session.averageHeat)%")
                gaugeRow(
                    label: "Last Temper",
                    value: viewModel.session.lastTemperedAt.map(Self.formatter.string(from:)) ?? "No temper stamp"
                )
            }

            Divider()

            VStack(alignment: .leading, spacing: 8) {
                Button("Open Ledger") {
                    viewModel.openLedgerPanel()
                }
                .keyboardShortcut("o", modifiers: [.command])
                .accessibilityLabel("Open ledger")

                Button("Stamp Ledger") {
                    viewModel.saveLedger()
                }
                .keyboardShortcut("s", modifiers: [.command])
                .accessibilityLabel("Stamp ledger")

                Button("Cast Bloom Manifest") {
                    viewModel.exportBloomManifest()
                }
                .keyboardShortcut("e", modifiers: [.command, .shift])
                .accessibilityLabel("Cast bloom manifest")
            }
            .buttonStyle(.borderedProminent)
            .tint(Color.forgeAmber)

            if let statusLine = viewModel.statusLine {
                Divider()
                Text(statusLine)
                    .font(.callout)
                    .foregroundStyle(Color.forgeSmoke)
                    .accessibilityLabel(statusLine)
            }

            Spacer(minLength: 0)
        }
        .padding(14)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .background(Color.forgePanel.opacity(0.35))
    }

    private func gaugeRow(label: String, value: String) -> some View {
        HStack {
            Text(label)
                .foregroundStyle(Color.forgeSmoke)
            Spacer()
            Text(value)
                .fontWeight(.semibold)
                .foregroundStyle(.primary)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(label): \(value)")
    }

    private static let formatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter
    }()
}
