Feature: Login functionality
  @positive
  Scenario Outline: Make Appointment
    Given the user already login
    When the user select facility with <facility>
    When the user check apply hospital readmission with <is_check_readmission>
    When the user select healthcare program with <healthcare_program>
    When the user select visit date with <visit_date>
    When the user fill comment with <comment>
    Then the user successfully made appointment

Examples:
  | facility                     | is_check_readmission  |  healthcare_program | visit_date | comment         |
  | Tokyo CURA Healthcare Center | true                  |  Medicare          | 07/07/2025 | medical checkup |