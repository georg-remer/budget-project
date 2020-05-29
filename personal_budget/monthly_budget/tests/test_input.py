TEST_TRANSACTIONS = [
    {
        'test_nr': 1,
        'input': {
            'date': '2018-03-21',
            'amount': '50',
            'description': 'Coffee to go',
            # ID for '6. Pocket Money' category = 13
            'outcome': 13
        },
        'expected_nr_of_transactions': 1,
        'output_transactions': [
            {
                'period': '2018 March',
                'date': '2018-03-21',
                'amount': '-50',
                'description': 'Coffee to go',
                'outcome': '6. Pocket Money',
                'income': None,
                'balance': '-50.00'
            }
        ],
        'output_balance': [
            {
                'period': '2018 March',
                'category': '6. Pocket Money',
                'planned_amount': '0.00',
                'income_amount': '0.00',
                'transferred_amount': '0.00',
                'spent_amount': '-50.00'
            }
        ]
    },
    {
        'test_nr': 2,
        'input': {
            'date': '2018-04-02',
            'amount': '100',
            'description': 'Sandwich',
            # ID for '6. Pocket Money' category = 13
            'outcome': 13
        },
        'expected_nr_of_transactions': 1,
        'output_transactions': [
            {
                'period': '2018 April',
                'date': '2018-04-02',
                'amount': '-100',
                'description': 'Sandwich',
                'outcome': '6. Pocket Money',
                'income': None,
                'balance': '-150.00'
            }
        ],
        'output_balance': [
            {
                'period': '2018 April',
                'category': '6. Pocket Money',
                'planned_amount': '0.00',
                'income_amount': '0.00',
                'transferred_amount': '0.00',
                'spent_amount': '-100.00'
            }
        ]
    },
    {
        'test_nr': 3,
        'input': {
            'date': '2019-10-01',
            'amount': '700',
            'description': 'A visit to a doctor',
            # ID for '7. Health' category = 14
            'outcome': 14,
            'income': None
        },
        'expected_nr_of_transactions': 1,
        'output_transactions': [
            {
                'period': '2019 October',
                'date': '2019-10-01',
                'amount': '-700',
                'description': 'A visit to a doctor',
                'outcome': '7. Health',
                'income': None,
                'balance': '-700.00'
            }
        ],
        'output_balance': [
            {
                'period': '2019 October',
                'category': '7. Health',
                'planned_amount': '0.00',
                'income_amount': '0.00',
                'transferred_amount': '0.00',
                'spent_amount': '-700.00'
            }
        ]
    },
    {
        'test_nr': 4,
        'input': {
            'date': '2019-10-03',
            'amount': '800.50',
            'description': 'Second visit to a doctor',
            # ID for '7. Health' category = 14
            'outcome': 14,
            'income': ''
        },
        'expected_nr_of_transactions': 1,
        'output_transactions': [
            {
                'period': '2019 October',
                'date': '2019-10-03',
                'amount': '-800.50',
                'description': 'Second visit to a doctor',
                'outcome': '7. Health',
                'income': None,
                'balance': '-1500.50'
            }
        ],
        'output_balance': [
            {
                'period': '2019 October',
                'category': '7. Health',
                'planned_amount': '0.00',
                'income_amount': '0.00',
                'transferred_amount': '0.00',
                'spent_amount': '-1500.50'
            }
        ]
    },
    {
        'test_nr': 5,
        'input': {
            'date': '2019-09-30',
            'amount': '30000',
            'description': 'Extra to savings',
            # ID for '14. Savings' category = 22
            'income': 22
        },
        'expected_nr_of_transactions': 1,
        'output_transactions': [
            {
                'period': '2019 September',
                'date': '2019-09-30',
                'amount': '30000',
                'description': 'Extra to savings',
                'outcome': None,
                'income': '14. Savings',
                'balance': '30000.00'
            }
        ],
        'output_balance': [
            {
                'period': '2019 September',
                'category': '14. Savings',
                'planned_amount': '0.00',
                'income_amount': '30000.00',
                'transferred_amount': '0.00',
                'spent_amount': '0.00'
            }
        ]
    },
    {
        'test_nr': 6,
        'input': {
            'date': '2019-10-11',
            'amount': '25600',
            'description': 'A trip to Europe',
            # ID for '14. Savings' category = 22
            'outcome': 22,
            # ID for '11. Vacation' category = 19
            'income': 19
        },
        'expected_nr_of_transactions': 2,
        'output_transactions': [
            {
                'period': '2019 October',
                'date': '2019-10-11',
                'amount': '-25600',
                'description': 'A trip to Europe',
                'outcome': '14. Savings',
                'income': None,
                'balance': '4400.00'
            },
            {
                'period': '2019 October',
                'date': '2019-10-11',
                'amount': '25600',
                'description': 'A trip to Europe',
                'outcome': None,
                'income': '11. Vacation',
                'balance': '25600.00'
            }
        ],
        'output_balance': [
            {
                'period': '2019 October',
                'category': '14. Savings',
                'planned_amount': '0.00',
                'income_amount': '0.00',
                'transferred_amount': '-25600.00',
                'spent_amount': '0.00'
            },
            {
                'period': '2019 October',
                'category': '11. Vacation',
                'planned_amount': '0.00',
                'income_amount': '25600.00',
                'transferred_amount': '0.00',
                'spent_amount': '0.00'
            }
        ]
    }
]
