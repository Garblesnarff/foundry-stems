import SwiftUI

struct ForgeSettingsView: View {
    @AppStorage("defaultAlloy") private var defaultAlloyRaw = StemAlloy.steel.rawValue
    @AppStorage("autoQuenchEnabled") private var autoQuenchEnabled = true
    @AppStorage("showSparkHints") private var showSparkHints = true
    @AppStorage("cacheLastHearth") private var cacheLastHearth = true

    var body: some View {
        Form {
            Section("Forge Defaults") {
                Picker("Default alloy", selection: $defaultAlloyRaw) {
                    ForEach(StemAlloy.allCases) { alloy in
                        Text(alloy.rawValue).tag(alloy.rawValue)
                    }
                }
                .accessibilityLabel("Default alloy")

                Toggle("Auto-quench ledger on every strike", isOn: $autoQuenchEnabled)
                    .accessibilityLabel("Auto-quench ledger on every strike")
                Toggle("Show spark hints while forging", isOn: $showSparkHints)
                    .accessibilityLabel("Show spark hints while forging")
                Toggle("Cache last hearth between launches", isOn: $cacheLastHearth)
                    .accessibilityLabel("Cache last hearth between launches")
            }

            Section("Sigil Placeholder") {
                Text(AppStoreShowcase.iconPlaceholderDescription)
                    .foregroundStyle(Color.forgeSmoke)
                    .textSelection(.enabled)
                    .accessibilityLabel(AppStoreShowcase.iconPlaceholderDescription)
            }

            Section("App Store Shot Drafts") {
                ForEach(AppStoreShowcase.shotDescriptions) { shot in
                    VStack(alignment: .leading, spacing: 4) {
                        Text(shot.title)
                            .font(.headline)
                            .foregroundStyle(Color.forgeAmber)
                        Text(shot.description)
                            .foregroundStyle(Color.forgeSmoke)
                    }
                    .padding(.vertical, 2)
                    .accessibilityElement(children: .combine)
                    .accessibilityLabel("\(shot.title): \(shot.description)")
                }
            }
        }
        .formStyle(.grouped)
        .scrollContentBackground(.hidden)
        .background(Color.forgeCharcoal)
    }
}
