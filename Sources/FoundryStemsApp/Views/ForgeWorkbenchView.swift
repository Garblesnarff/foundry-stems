import SwiftUI

struct ForgeWorkbenchView: View {
    @ObservedObject var viewModel: ForgeViewModel

    var body: some View {
        ZStack(alignment: .top) {
            NavigationSplitView {
                BilletRackView(viewModel: viewModel)
            } content: {
                BilletDetailView(viewModel: viewModel)
            } detail: {
                ForgeInspectorView(viewModel: viewModel)
            }
            .navigationSplitViewStyle(.balanced)
            .background(Color.forgeCharcoal)
            .dropDestination(for: URL.self) { urls, _ in
                viewModel.ingestDroppedFiles(urls)
                return true
            } isTargeted: { isTargeted in
                viewModel.isDropTargeted = isTargeted
            }

            if viewModel.isDropTargeted {
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(Color.forgeAmber.opacity(0.15))
                    .stroke(Color.forgeAmber, lineWidth: 2)
                    .overlay {
                        Text("Drop ore files to charge the hearth")
                            .foregroundStyle(Color.forgeAmber)
                            .font(.headline)
                    }
                    .padding(28)
                    .allowsHitTesting(false)
                    .accessibilityLabel("Drop ore files to charge the hearth")
            }

            if let forgeFault = viewModel.forgeFault {
                ForgeFaultBanner(message: forgeFault) {
                    viewModel.clearFault()
                }
                .padding(.top, 10)
                .padding(.horizontal, 12)
                .transition(.move(edge: .top).combined(with: .opacity))
            }
        }
        .background(Color.forgeCharcoal.ignoresSafeArea())
    }
}
