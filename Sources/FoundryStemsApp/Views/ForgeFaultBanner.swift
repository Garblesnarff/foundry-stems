import SwiftUI

struct ForgeFaultBanner: View {
    let message: String
    let onDismiss: () -> Void

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundStyle(Color.forgeAmber)
                .accessibilityHidden(true)
            Text("Forge fault: \(message)")
                .foregroundStyle(.white)
                .font(.callout)
                .lineLimit(3)
            Spacer(minLength: 8)
            Button("Clear Ember", action: onDismiss)
                .buttonStyle(.bordered)
                .tint(Color.forgeAmber)
                .accessibilityLabel("Clear forge fault")
        }
        .padding(12)
        .background(Color.black.opacity(0.78))
        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
        .shadow(color: .black.opacity(0.45), radius: 8, y: 4)
        .accessibilityElement(children: .combine)
    }
}
