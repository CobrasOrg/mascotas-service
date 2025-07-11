module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat", // Nueva característica
        "fix", // Corrección de bug
        "docs", // Cambios en documentación
        "style", // Cambios que no afectan el significado del código
        "refactor", // Refactorización de código
        "perf", // Cambios que mejoran el rendimiento
        "test", // Añadir o corregir tests
        "build", // Cambios que afectan al sistema de build
        "ci", // Cambios en archivos de configuración de CI
        "chore", // Otros cambios que no modifican src o test
        "revert", // Revertir un commit
      ],
    ],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "subject-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 72],
  },
};
