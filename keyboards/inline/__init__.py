from .directions_menu import (directions_callback_data, all_directions_inlines, delete_direction_inlines,
                              direction_inlines)
from .types_edu_menu import (types_callback_data, all_types_of_edu_inlines, type_of_edu_inlines,
                             delete_type_of_edu_inlines)
from .contracts_menu import (contracts_callback_data, all_directions_for_contract_inlines,
                             all_types_for_contract_inlines, all_contract_prices_inlines, detail_contract_inlines,
                             delete_contract_inlines)
from .applicant_inlines import (application_callback_data, all_faculties_inlines, types_and_contracts,
                                choices_e_edu_language)
from .you_are_ready import ready_inline_button
from .question_responses import responses_callback_data, all_responses_inlines
from .sciences_inlines import science_callback_data, science_list_markup, science_show_markup, request_deletion_markup
from .tests_inlines import (all_science_inlines_for_test, lang_inlines_for_test, test_markup,
                            test_callback_data, all_sciences_markup, tests_for_science_markup,
                            question_delete_test_markup, questions_list_markup, question_markup,
                            question_delete_question_markup)
