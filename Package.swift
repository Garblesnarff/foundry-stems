// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "FoundryStems",
    platforms: [
        .macOS(.v14)
    ],
    products: [
        .executable(
            name: "FoundryStems",
            targets: ["FoundryStemsApp"]
        )
    ],
    targets: [
        .executableTarget(
            name: "FoundryStemsApp",
            path: "Sources/FoundryStemsApp",
            resources: [.process("PrivacyInfo.xcprivacy")],
        ),
        .testTarget(
            name: "FoundryStemsAppTests",
            dependencies: ["FoundryStemsApp"],
            path: "Tests/FoundryStemsAppTests"
        )
    ]
)
