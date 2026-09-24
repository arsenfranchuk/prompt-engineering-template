# Budgets — Business Requirements

## Purpose
Enable users to set planned spending targets for specific expense categories across defined time periods (e.g. monthly), track actual spending vs. target in real time, and receive clear visual warnings when nearing or exceeding budget limits.

## Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-BDG-01 | Create a budget for an expense category with a planned positive amount and period (e.g. monthly with start and end dates). | Full Stack |
| BR-BDG-02 | Prevent multiple active overlapping budgets for the exact same category and time window. | Backend |
| BR-BDG-03 | Calculate actual spent amount dynamically from stored expense transactions matching the category and budget date window. | Backend |
| BR-BDG-04 | Calculate remaining amount (`planned - spent`) and percentage used (`(spent / planned) * 100`). | Backend & Full Stack |
| BR-BDG-05 | Display budget status: `within` (< 80%), `warning` (80% to 100%), and `exceeded` (> 100%). | Full Stack |
| BR-BDG-06 | Visual progress bar with dynamic color indicators: Green for within, Amber/Yellow for approaching limit, Red for exceeded. | Frontend |
| BR-BDG-07 | Edit existing budget (modify planned amount or period). | Full Stack |
| BR-BDG-08 | Delete budget with confirmation. | Full Stack |
| BR-BDG-09 | Strict isolation: only the owner can view or modify their budgets. | Backend |
