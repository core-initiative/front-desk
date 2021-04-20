def get_account():
	accounts = [
		{
			"account_name": "Asset",
			"parent_number": "",
			"account_number": "1000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Current Asset",
			"parent_number": "1000.000",
			"account_number": "1100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Cash",
			"parent_number": "1100.000",
			"account_number": "1110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Rupiah Cash",
			"parent_number": "1110.000",
			"account_number": "1111.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "House Bank General Cashier",
			"parent_number": "1111.000",
			"account_number": "1111.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "House Bank Resto",
			"parent_number": "1111.000",
			"account_number": "1111.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "House Bank Front Office",
			"parent_number": "1111.000",
			"account_number": "1111.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "Other Currency Cash",
			"parent_number": "1110.000",
			"account_number": "1112.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "USD Cash",
			"parent_number": "1112.000",
			"account_number": "1112.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "Cash Clearance",
			"parent_number": "1110.000",
			"account_number": "1113.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank",
			"parent_number": "1100.000",
			"account_number": "1120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank Rupiah",
			"parent_number": "1120.000",
			"account_number": "1121.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "BCA",
			"parent_number": "1121.000",
			"account_number": "1121.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank Mandiri",
			"parent_number": "1121.000",
			"account_number": "1121.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank CIMB Niaga",
			"parent_number": "1121.000",
			"account_number": "1121.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank BRI",
			"parent_number": "1121.000",
			"account_number": "1121.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank BNI",
			"parent_number": "1121.000",
			"account_number": "1121.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "CC Mega",
			"parent_number": "1121.000",
			"account_number": "1121.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Bank Other Currency",
			"parent_number": "1120.000",
			"account_number": "1122.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Account Receivable",
			"parent_number": "1100.000",
			"account_number": "1130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "A/R Bank",
			"parent_number": "1130.000",
			"account_number": "1131.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "BCA Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Mandiri Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "CIMB Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "BRI Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "BNI Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "A/R Card and e-Payment",
			"parent_number": "1130.000",
			"account_number": "1132.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "BCA EDC",
			"parent_number": "1132.000",
			"account_number": "1132.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "Mandiri EDC",
			"parent_number": "1132.000",
			"account_number": "1132.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "BRI EDC",
			"parent_number": "1132.000",
			"account_number": "1132.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "BNI EDC",
			"parent_number": "1132.000",
			"account_number": "1132.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "CIMB Niaga EDC",
			"parent_number": "1132.000",
			"account_number": "1132.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Asset"
		},
		{
			"account_name": "OVO",
			"parent_number": "1132.000",
			"account_number": "1132.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Dana",
			"parent_number": "1132.000",
			"account_number": "1132.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Cashbac",
			"parent_number": "1132.000",
			"account_number": "1132.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Other A/R",
			"parent_number": "1130.000",
			"account_number": "1133.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "A/R City Ledger",
			"parent_number": "1133.000",
			"account_number": "1133.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "A/R Sale",
			"parent_number": "1133.000",
			"account_number": "1133.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable",
			"root_type": "Asset"
		},
		{
			"account_name": "A/R Guest Ledger",
			"parent_number": "1133.000",
			"account_number": "1133.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable",
			"root_type": "Asset"
		},
		{
			"account_name": "Inventory",
			"parent_number": "1100.000",
			"account_number": "1140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Hotel Inventory",
			"parent_number": "1140.000",
			"account_number": "1141.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Stock",
			"root_type": "Asset"
		},
		{
			"account_name": "Store Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "House keeping Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock",
			"root_type": "Asset"
		},
		{
			"account_name": "Engineering Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock",
			"root_type": "Asset"
		},
		{
			"account_name": "Prepaid Expense",
			"parent_number": "1100.000",
			"account_number": "1150.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Prepaid Tax",
			"parent_number": "1150.000",
			"account_number": "1151.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Prepaid Rent",
			"parent_number": "1150.000",
			"account_number": "1152.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Other Prepaid",
			"parent_number": "1150.000",
			"account_number": "1153.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Temporary Account",
			"parent_number": "1100.000",
			"account_number": "1170.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Temporary Opening",
			"parent_number": "1170.000",
			"account_number": "1171.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Temporary",
			"root_type": "Asset"
		},
		{
			"account_name": "Deposit Customer",
			"parent_number": "1170.000",
			"account_number": "1172.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Fixed Asset",
			"parent_number": "1000.000",
			"account_number": "1200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Asset",
			"parent_number": "1200.000",
			"account_number": "1210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Property and Equipment",
			"parent_number": "1210.000",
			"account_number": "1211.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Land",
			"parent_number": "1211.000",
			"account_number": "1211.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Building",
			"parent_number": "1211.000",
			"account_number": "1211.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Vehicle",
			"parent_number": "1211.000",
			"account_number": "1211.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Computer and Hardware",
			"parent_number": "1211.000",
			"account_number": "1211.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Air Conditioning",
			"parent_number": "1211.000",
			"account_number": "1211.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Machinery",
			"parent_number": "1211.000",
			"account_number": "1211.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Electronic and Mechanical",
			"parent_number": "1211.000",
			"account_number": "1211.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Office Equipment",
			"parent_number": "1211.000",
			"account_number": "1211.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Accumulated Depreciation of Asset",
			"parent_number": "1210.000",
			"account_number": "1212.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Accumulated Depreciation of Assets",
			"parent_number": "1212.000",
			"account_number": "1212.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Accumulated Depreciation",
			"root_type": "Asset"
		},
		{
			"account_name": "Deposit Alistair",
			"parent_number": "1212.000",
			"account_number": "1212.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Depreciation",
			"root_type": "Asset"
		},
		{
			"account_name": "Allowance for Doubtful Account",
			"parent_number": "1212.000",
			"account_number": "1212.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Depreciation",
			"root_type": "Asset"
		},
		{
			"account_name": "Furniture, Fixture and Equipment",
			"parent_number": "1210.000",
			"account_number": "1213.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Room",
			"parent_number": "1213.000",
			"account_number": "1213.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Food and Beverages",
			"parent_number": "1213.000",
			"account_number": "1213.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Human Resource",
			"parent_number": "1213.000",
			"account_number": "1213.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Sales and Marketing",
			"parent_number": "1213.000",
			"account_number": "1213.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Engineering",
			"parent_number": "1213.000",
			"account_number": "1213.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "FF&E Administration and General",
			"parent_number": "1213.000",
			"account_number": "1213.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Operating Equipment",
			"parent_number": "1210.000",
			"account_number": "1214.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Linen Room",
			"parent_number": "1214.000",
			"account_number": "1214.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Linen FB",
			"parent_number": "1214.000",
			"account_number": "1214.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Chinaware Room",
			"parent_number": "1214.000",
			"account_number": "1214.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Chinaware FB",
			"parent_number": "1214.000",
			"account_number": "1214.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Glassware Room",
			"parent_number": "1214.000",
			"account_number": "1214.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Glassware FB",
			"parent_number": "1214.000",
			"account_number": "1214.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Silverware Room",
			"parent_number": "1214.000",
			"account_number": "1214.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Silverware FB",
			"parent_number": "1214.000",
			"account_number": "1214.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Kitchen Utensils",
			"parent_number": "1214.000",
			"account_number": "1214.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Uniform Room",
			"parent_number": "1214.000",
			"account_number": "1214.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Uniform FB",
			"parent_number": "1214.000",
			"account_number": "1214.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Administration & General",
			"parent_number": "1214.000",
			"account_number": "1214.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Human Resource",
			"parent_number": "1214.000",
			"account_number": "1214.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Sales and Marketing",
			"parent_number": "1214.000",
			"account_number": "1214.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Room",
			"parent_number": "1214.000",
			"account_number": "1214.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp House Keeping",
			"parent_number": "1214.000",
			"account_number": "1214.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Resto",
			"parent_number": "1214.000",
			"account_number": "1214.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Opr. Eqp Other",
			"parent_number": "1214.000",
			"account_number": "1214.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset",
			"root_type": "Asset"
		},
		{
			"account_name": "Liabilities",
			"parent_number": "",
			"account_number": "2000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Current Liabilities",
			"parent_number": "2000.000",
			"account_number": "2100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Account Payable",
			"parent_number": "2100.000",
			"account_number": "2110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Stock Received But Not Billed",
			"parent_number": "2110.000",
			"account_number": "2110.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock Received But Not Billed",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Trade",
			"parent_number": "2110.000",
			"account_number": "2110.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Short Term Loan",
			"parent_number": "2110.000",
			"account_number": "2110.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Service Charge",
			"parent_number": "2110.000",
			"account_number": "2110.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Guest Deposit",
			"parent_number": "2110.000",
			"account_number": "2110.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Loss and Breakage - 5%",
			"parent_number": "2110.000",
			"account_number": "2110.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P HR Development - 2%",
			"parent_number": "2110.000",
			"account_number": "2110.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Payable Commission",
			"parent_number": "2110.000",
			"account_number": "2110.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Tips",
			"parent_number": "2110.000",
			"account_number": "2110.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Clearance",
			"parent_number": "2110.000",
			"account_number": "2110.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Owner",
			"parent_number": "2110.000",
			"account_number": "2110.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Other",
			"parent_number": "2110.000",
			"account_number": "2110.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P In Transit",
			"parent_number": "2110.000",
			"account_number": "2110.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/P Voucher",
			"parent_number": "2110.000",
			"account_number": "2110.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable",
			"root_type": "Liability"
		},
		{
			"account_name": "Prepaid Income",
			"parent_number": "2100.000",
			"account_number": "2120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Prepaid Income",
			"parent_number": "2120.000",
			"account_number": "2121.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "DP Sales",
			"parent_number": "2121.000",
			"account_number": "2121.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Liability"
		},
		{
			"account_name": "DP Room",
			"parent_number": "2121.000",
			"account_number": "2121.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Accrued Expense",
			"parent_number": "2100.000",
			"account_number": "2130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Accrued Expense",
			"parent_number": "2130.000",
			"account_number": "2131.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Electricity",
			"parent_number": "2131.000",
			"account_number": "2131.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Contract Agreement",
			"parent_number": "2131.000",
			"account_number": "2131.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Telephone",
			"parent_number": "2131.000",
			"account_number": "2131.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Water",
			"parent_number": "2131.000",
			"account_number": "2131.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Internet",
			"parent_number": "2131.000",
			"account_number": "2131.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Salary",
			"parent_number": "2131.000",
			"account_number": "2131.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Insurance",
			"parent_number": "2131.000",
			"account_number": "2131.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Medical",
			"parent_number": "2131.000",
			"account_number": "2131.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Jamsostek",
			"parent_number": "2131.000",
			"account_number": "2131.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E TV Channel",
			"parent_number": "2131.000",
			"account_number": "2131.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Laundry",
			"parent_number": "2131.000",
			"account_number": "2131.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Meal",
			"parent_number": "2131.000",
			"account_number": "2131.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Music and Entertainment",
			"parent_number": "2131.000",
			"account_number": "2131.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Newspaper and Magazine",
			"parent_number": "2131.000",
			"account_number": "2131.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Transportation",
			"parent_number": "2131.000",
			"account_number": "2131.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Commission",
			"parent_number": "2131.000",
			"account_number": "2131.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Audit",
			"parent_number": "2131.000",
			"account_number": "2131.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Pest Control",
			"parent_number": "2131.000",
			"account_number": "2131.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Garbage Cleaning",
			"parent_number": "2131.000",
			"account_number": "2131.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Removal of Waste",
			"parent_number": "2131.000",
			"account_number": "2131.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Elevator",
			"parent_number": "2131.000",
			"account_number": "2131.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E S&M Fee",
			"parent_number": "2131.000",
			"account_number": "2131.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Incentive Fee",
			"parent_number": "2131.000",
			"account_number": "2131.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Management Fee",
			"parent_number": "2131.000",
			"account_number": "2131.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Room Department",
			"parent_number": "2131.000",
			"account_number": "2131.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E FB Department",
			"parent_number": "2131.000",
			"account_number": "2131.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E HR Department",
			"parent_number": "2131.000",
			"account_number": "2131.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Accounting Department",
			"parent_number": "2131.000",
			"account_number": "2131.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Sales and Marketing Department",
			"parent_number": "2131.000",
			"account_number": "2131.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Engineering Department",
			"parent_number": "2131.000",
			"account_number": "2131.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Security Department",
			"parent_number": "2131.000",
			"account_number": "2131.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Contract Cleaning",
			"parent_number": "2131.000",
			"account_number": "2131.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Petty Cash",
			"parent_number": "2131.000",
			"account_number": "2131.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Daily Worker",
			"parent_number": "2131.000",
			"account_number": "2131.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Outsourcing",
			"parent_number": "2131.000",
			"account_number": "2131.035",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E Other",
			"parent_number": "2131.000",
			"account_number": "2131.036",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "A/E BPJS Ketenagakerjaan",
			"parent_number": "2131.000",
			"account_number": "2131.037",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Tax Payable",
			"parent_number": "2100.000",
			"account_number": "2140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Reconstruction Tax - PB 1",
			"parent_number": "2140.000",
			"account_number": "2141.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax",
			"root_type": "Liability"
		},
		{
			"account_name": "Land & Building Tax",
			"parent_number": "2140.000",
			"account_number": "2142.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax",
			"root_type": "Liability"
		},
		{
			"account_name": "Fixed Asset",
			"parent_number": "2000.000",
			"account_number": "2200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Debt to Third Parties",
			"parent_number": "2200.000",
			"account_number": "2210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Routine Third Party Loan",
			"parent_number": "2210.000",
			"account_number": "2211.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Shareholder Loan",
			"parent_number": "2211.000",
			"account_number": "2211.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Routine Loan",
			"parent_number": "2211.000",
			"account_number": "2211.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Non-routine Third Party Loan",
			"parent_number": "2210.000",
			"account_number": "2212.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Shareholder Loan",
			"parent_number": "2212.000",
			"account_number": "2212.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Non-routine Loan",
			"parent_number": "2212.000",
			"account_number": "2212.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Non-routine Third Party Loan Interest Debt",
			"parent_number": "2210.000",
			"account_number": "2213.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Interest Debt",
			"parent_number": "2213.000",
			"account_number": "2213.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Debt to Bank",
			"parent_number": "2200.000",
			"account_number": "2220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Bank Loan",
			"parent_number": "2220.000",
			"account_number": "2221.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Bank Loan",
			"parent_number": "2221.000",
			"account_number": "2221.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Leasing Debt",
			"parent_number": "2200.000",
			"account_number": "2230.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Leasing Debt",
			"parent_number": "2230.000",
			"account_number": "2231.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Vehicle Leasing",
			"parent_number": "2231.000",
			"account_number": "2231.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Other Leasing",
			"parent_number": "2231.000",
			"account_number": "2231.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Other Debt",
			"parent_number": "2200.000",
			"account_number": "2240.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Other Debt",
			"parent_number": "2240.000",
			"account_number": "2241.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Debt",
			"parent_number": "2241.000",
			"account_number": "2241.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Liability"
		},
		{
			"account_name": "Capital",
			"parent_number": "",
			"account_number": "3000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Capital",
			"parent_number": "3000.000",
			"account_number": "3100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Paid Up Capital",
			"parent_number": "3100.000",
			"account_number": "3110.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Shareholder",
			"parent_number": "3100.000",
			"account_number": "3120.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Opening Balance of Equity",
			"parent_number": "3100.000",
			"account_number": "3130.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Withdrawal",
			"parent_number": "3100.000",
			"account_number": "3140.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Earning",
			"parent_number": "3000.000",
			"account_number": "3200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Retained Earning",
			"parent_number": "3200.000",
			"account_number": "3210.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Profit and Loss Current Period",
			"parent_number": "3200.000",
			"account_number": "3220.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Profit and Loss Last Year",
			"parent_number": "3200.000",
			"account_number": "3230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Prior Year Adjustment",
			"parent_number": "3200.000",
			"account_number": "3240.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Equity"
		},
		{
			"account_name": "Revenue",
			"parent_number": "",
			"account_number": "4000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Food and Beverages Revenue",
			"parent_number": "4000.000",
			"account_number": "4100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Kitchen Revenue",
			"parent_number": "4100.000",
			"account_number": "4110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Breakfast Revenue",
			"parent_number": "4110.000",
			"account_number": "4110.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Restaurant Revenue",
			"parent_number": "4100.000",
			"account_number": "4120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Restaurant Food Revenue",
			"parent_number": "4120.000",
			"account_number": "4120.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Restaurant Beverages Revenue",
			"parent_number": "4120.000",
			"account_number": "4120.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Lounge Revenue",
			"parent_number": "4100.000",
			"account_number": "4130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Lounge Food Revenue",
			"parent_number": "4130.000",
			"account_number": "4130.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Lounge Beverages Revenue",
			"parent_number": "4130.000",
			"account_number": "4130.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Room Service Revenue",
			"parent_number": "4100.000",
			"account_number": "4140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Room Service Food Revenue",
			"parent_number": "4140.000",
			"account_number": "4140.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Room Service Beverages Revenue",
			"parent_number": "4140.000",
			"account_number": "4140.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Revenue",
			"parent_number": "4100.000",
			"account_number": "4150.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Lunch Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Dinner Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Coffee Break Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Meeting",
			"parent_number": "4150.000",
			"account_number": "4150.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Other Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Banquet Wedding Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Other Food and Beverages Revenue",
			"parent_number": "4100.000",
			"account_number": "4160.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Room Revenue",
			"parent_number": "4000.000",
			"account_number": "4200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Front Office Revenue",
			"parent_number": "4200.000",
			"account_number": "4210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Room Revenue",
			"parent_number": "4210.000",
			"account_number": "4210.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "House Keeping Revenue",
			"parent_number": "4200.000",
			"account_number": "4220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Guest Laundry Revenue",
			"parent_number": "4220.000",
			"account_number": "4220.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Public Laundry Revenue",
			"parent_number": "4220.000",
			"account_number": "4220.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Other Room Revenue",
			"parent_number": "4200.000",
			"account_number": "4230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Other Revenue",
			"parent_number": "4000.000",
			"account_number": "4300.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Income"
		},
		{
			"account_name": "Rounding Off",
			"parent_number": "4300.000",
			"account_number": "4300.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Foreign Exchange Earned",
			"parent_number": "4300.000",
			"account_number": "4300.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Interest Income",
			"parent_number": "4300.000",
			"account_number": "4300.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Revenue from Warehouse",
			"parent_number": "4300.000",
			"account_number": "4300.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account",
			"root_type": "Income"
		},
		{
			"account_name": "Cost of Sale",
			"parent_number": "",
			"account_number": "5000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Food and Beverage Cost",
			"parent_number": "5000.000",
			"account_number": "5100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Food Cost",
			"parent_number": "5100.000",
			"account_number": "5110.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold",
			"root_type": "Expense"
		},
		{
			"account_name": "Beverage Cost",
			"parent_number": "5100.000",
			"account_number": "5120.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold",
			"root_type": "Expense"
		},
		{
			"account_name": "Grab Food Cost",
			"parent_number": "5100.000",
			"account_number": "5130.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Room Cost",
			"parent_number": "5000.000",
			"account_number": "5200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Cost of Front Office",
			"parent_number": "5200.000",
			"account_number": "5210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Cost of Guest Supplies",
			"parent_number": "5210.000",
			"account_number": "5210.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold",
			"root_type": "Expense"
		},
		{
			"account_name": "Cost of House Keeping",
			"parent_number": "5200.000",
			"account_number": "5220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Cost of Laundry",
			"parent_number": "5220.000",
			"account_number": "5220.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Other Room Cost",
			"parent_number": "5200.000",
			"account_number": "5230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Expenses",
			"parent_number": "",
			"account_number": "6000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Salary and Wages",
			"parent_number": "6000.000",
			"account_number": "6100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "F&B Department Salary",
			"parent_number": "6100.000",
			"account_number": "6101.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Room Department Salary",
			"parent_number": "6100.000",
			"account_number": "6102.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Equity",
			"root_type": "Expense"
		},
		{
			"account_name": "Sales and Marketing Department Salary",
			"parent_number": "6100.000",
			"account_number": "6103.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HR Department Salary",
			"parent_number": "6100.000",
			"account_number": "6104.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Department Salary",
			"parent_number": "6100.000",
			"account_number": "6105.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Accounting Department Salary",
			"parent_number": "6100.000",
			"account_number": "6106.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Department Salary",
			"parent_number": "6100.000",
			"account_number": "6107.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Department Salary",
			"parent_number": "6100.000",
			"account_number": "6108.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Daily Worker Wages",
			"parent_number": "6100.000",
			"account_number": "6109.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Employee Benefit",
			"parent_number": "6000.000",
			"account_number": "6200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Employee Insurance Cost",
			"parent_number": "6200.000",
			"account_number": "6201.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Employee Medical Expense",
			"parent_number": "6200.000",
			"account_number": "6202.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Employee Meal Expense",
			"parent_number": "6200.000",
			"account_number": "6203.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "THR Cost, Benefits, Commission",
			"parent_number": "6200.000",
			"account_number": "6204.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Uniform Cost",
			"parent_number": "6200.000",
			"account_number": "6205.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Training Cost",
			"parent_number": "6200.000",
			"account_number": "6206.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Entertainment Expense",
			"parent_number": "6200.000",
			"account_number": "6207.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Other Employee Cost",
			"parent_number": "6200.000",
			"account_number": "6208.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Other Expense",
			"parent_number": "6000.000",
			"account_number": "6920.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Voucher Payment",
			"parent_number": "6920.000",
			"account_number": "6920.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank",
			"root_type": "Expense"
		},
		{
			"account_name": "Legal",
			"parent_number": "6920.000",
			"account_number": "6920.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6010.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Daily Worker Salary",
			"parent_number": "6010.000",
			"account_number": "6010.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Salaries & Wages",
			"parent_number": "6010.000",
			"account_number": "6010.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Jamsostek",
			"parent_number": "6010.000",
			"account_number": "6010.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Casual Worker",
			"parent_number": "6010.000",
			"account_number": "6010.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Bonus/THR",
			"parent_number": "6010.000",
			"account_number": "6010.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Employee Meals",
			"parent_number": "6010.000",
			"account_number": "6010.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Payroll Taxes & Benefits",
			"parent_number": "6010.000",
			"account_number": "6010.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Medical",
			"parent_number": "6010.000",
			"account_number": "6010.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Staff Transportation/Relocation",
			"parent_number": "6010.000",
			"account_number": "6010.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO BPJS Kesehatan",
			"parent_number": "6010.000",
			"account_number": "6010.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6020.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "FO China,Glass,Silver",
			"parent_number": "6020.000",
			"account_number": "6020.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Linen",
			"parent_number": "6020.000",
			"account_number": "6020.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Cleaning Supplies",
			"parent_number": "6020.000",
			"account_number": "6020.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Guest Supplies",
			"parent_number": "6020.000",
			"account_number": "6020.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Paper Supplies",
			"parent_number": "6020.000",
			"account_number": "6020.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Uniforms",
			"parent_number": "6020.000",
			"account_number": "6020.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Decoration",
			"parent_number": "6020.000",
			"account_number": "6020.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Menus",
			"parent_number": "6020.000",
			"account_number": "6020.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Systems Support",
			"parent_number": "6020.000",
			"account_number": "6020.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Other Supplies",
			"parent_number": "6020.000",
			"account_number": "6020.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Telephone & Fax",
			"parent_number": "6020.000",
			"account_number": "6020.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Contract Services",
			"parent_number": "6020.000",
			"account_number": "6020.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Travel & Entertainment",
			"parent_number": "6020.000",
			"account_number": "6020.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Transportation",
			"parent_number": "6020.000",
			"account_number": "6020.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Other Professional Services",
			"parent_number": "6020.000",
			"account_number": "6020.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Postage / Express",
			"parent_number": "6020.000",
			"account_number": "6020.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Dues & Subscription",
			"parent_number": "6020.000",
			"account_number": "6020.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Training",
			"parent_number": "6020.000",
			"account_number": "6020.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Equipment Rental",
			"parent_number": "6020.000",
			"account_number": "6020.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Licenses & Fees",
			"parent_number": "6020.000",
			"account_number": "6020.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Printing & Stationary",
			"parent_number": "6020.000",
			"account_number": "6020.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Music & Entertainment",
			"parent_number": "6020.000",
			"account_number": "6020.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Other Expenses",
			"parent_number": "6020.000",
			"account_number": "6020.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Laundry & Dry Cleaning Linen",
			"parent_number": "6020.000",
			"account_number": "6020.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Laundry & Dry Cleaning Uniform",
			"parent_number": "6020.000",
			"account_number": "6020.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Guest Transportation",
			"parent_number": "6020.000",
			"account_number": "6020.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Travel Agency Commission",
			"parent_number": "6020.000",
			"account_number": "6020.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Cable & TV Satelite",
			"parent_number": "6020.000",
			"account_number": "6020.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Laundry",
			"parent_number": "6020.000",
			"account_number": "6020.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Complimentary Breakfast",
			"parent_number": "6020.000",
			"account_number": "6020.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Systems Support / Internet",
			"parent_number": "6020.000",
			"account_number": "6020.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Comp. Welcome Drink",
			"parent_number": "6020.000",
			"account_number": "6020.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Comp. Fruit Basket & B'day Cake",
			"parent_number": "6020.000",
			"account_number": "6020.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FO Entertainment",
			"parent_number": "6020.000",
			"account_number": "6020.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Salaries & Wages",
			"parent_number": "6110.000",
			"account_number": "6110.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Jamsostek",
			"parent_number": "6110.000",
			"account_number": "6110.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Casual Worker",
			"parent_number": "6110.000",
			"account_number": "6110.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Bonus/THR",
			"parent_number": "6110.000",
			"account_number": "6110.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Employee Meals",
			"parent_number": "6110.000",
			"account_number": "6110.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Payroll Taxes & Benefits",
			"parent_number": "6110.000",
			"account_number": "6110.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Medical",
			"parent_number": "6110.000",
			"account_number": "6110.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Staff Transportation/Relocation",
			"parent_number": "6110.000",
			"account_number": "6110.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Daily Worker Salary",
			"parent_number": "6110.000",
			"account_number": "6110.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK BPJS Kesehatan",
			"parent_number": "6110.000",
			"account_number": "6110.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "HK China,Glass,Silver",
			"parent_number": "6120.000",
			"account_number": "6120.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Linen",
			"parent_number": "6120.000",
			"account_number": "6120.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Cleaning Supplies",
			"parent_number": "6120.000",
			"account_number": "6120.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Guest Supplies",
			"parent_number": "6120.000",
			"account_number": "6120.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Paper Supplies",
			"parent_number": "6120.000",
			"account_number": "6120.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Uniforms",
			"parent_number": "6120.000",
			"account_number": "6120.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Decoration",
			"parent_number": "6120.000",
			"account_number": "6120.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Menus",
			"parent_number": "6120.000",
			"account_number": "6120.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Pest Control",
			"parent_number": "6120.000",
			"account_number": "6120.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Other Supplies",
			"parent_number": "6120.000",
			"account_number": "6120.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Telephone & Fax",
			"parent_number": "6120.000",
			"account_number": "6120.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Contract Services",
			"parent_number": "6120.000",
			"account_number": "6120.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Travel & Entertainment",
			"parent_number": "6120.000",
			"account_number": "6120.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Transportation",
			"parent_number": "6120.000",
			"account_number": "6120.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Other Professional Services",
			"parent_number": "6120.000",
			"account_number": "6120.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Postage / Express",
			"parent_number": "6120.000",
			"account_number": "6120.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Dues & Subscription",
			"parent_number": "6120.000",
			"account_number": "6120.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Training",
			"parent_number": "6120.000",
			"account_number": "6120.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Equipment Rental",
			"parent_number": "6120.000",
			"account_number": "6120.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Licenses & Fees",
			"parent_number": "6120.000",
			"account_number": "6120.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Printing & Stationary",
			"parent_number": "6120.000",
			"account_number": "6120.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Music & Entertainment",
			"parent_number": "6120.000",
			"account_number": "6120.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Other Expenses",
			"parent_number": "6120.000",
			"account_number": "6120.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Laundry & Dry Cleaning Linen",
			"parent_number": "6120.000",
			"account_number": "6120.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Laundry & Dry Cleaning Uniform",
			"parent_number": "6120.000",
			"account_number": "6120.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Guest Transportation",
			"parent_number": "6120.000",
			"account_number": "6120.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Travel Agency Commission",
			"parent_number": "6120.000",
			"account_number": "6120.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Cable & TV Satelite",
			"parent_number": "6120.000",
			"account_number": "6120.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Laundry",
			"parent_number": "6120.000",
			"account_number": "6120.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Complimentary Breakfast",
			"parent_number": "6120.000",
			"account_number": "6120.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Systems Support / Internet",
			"parent_number": "6120.000",
			"account_number": "6120.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Comp. Welcome Drink",
			"parent_number": "6120.000",
			"account_number": "6120.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Comp. Fruit Basket & B'day Cake",
			"parent_number": "6120.000",
			"account_number": "6120.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HK Entertainment",
			"parent_number": "6120.000",
			"account_number": "6120.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Salaries & Wages",
			"parent_number": "6210.000",
			"account_number": "6210.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Jamsostek",
			"parent_number": "6210.000",
			"account_number": "6210.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Casual Worker",
			"parent_number": "6210.000",
			"account_number": "6210.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Bonus/THR",
			"parent_number": "6210.000",
			"account_number": "6210.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Employee Meals",
			"parent_number": "6210.000",
			"account_number": "6210.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Payroll Taxes & Benefits",
			"parent_number": "6210.000",
			"account_number": "6210.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Medical",
			"parent_number": "6210.000",
			"account_number": "6210.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Staff Transportation",
			"parent_number": "6210.000",
			"account_number": "6210.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Daily Worker Salary",
			"parent_number": "6210.000",
			"account_number": "6210.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO BPJS Kesehatan",
			"parent_number": "6210.000",
			"account_number": "6210.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO China,Glass,Silver",
			"parent_number": "6220.000",
			"account_number": "6220.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Linen",
			"parent_number": "6220.000",
			"account_number": "6220.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Cleaning Supplies",
			"parent_number": "6220.000",
			"account_number": "6220.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Guest Supplies",
			"parent_number": "6220.000",
			"account_number": "6220.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Paper Supplies",
			"parent_number": "6220.000",
			"account_number": "6220.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Uniforms",
			"parent_number": "6220.000",
			"account_number": "6220.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Decorations",
			"parent_number": "6220.000",
			"account_number": "6220.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Menus",
			"parent_number": "6220.000",
			"account_number": "6220.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Telephone",
			"parent_number": "6220.000",
			"account_number": "6220.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Contract Services",
			"parent_number": "6220.000",
			"account_number": "6220.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Entertainment",
			"parent_number": "6220.000",
			"account_number": "6220.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Transportation",
			"parent_number": "6220.000",
			"account_number": "6220.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Special Promotion",
			"parent_number": "6220.000",
			"account_number": "6220.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Postage / Express",
			"parent_number": "6220.000",
			"account_number": "6220.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Bar Supplies",
			"parent_number": "6220.000",
			"account_number": "6220.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Training",
			"parent_number": "6220.000",
			"account_number": "6220.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Equipment Rental",
			"parent_number": "6220.000",
			"account_number": "6220.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Licenses Fees",
			"parent_number": "6220.000",
			"account_number": "6220.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Printing & Stationary",
			"parent_number": "6220.000",
			"account_number": "6220.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Music & Entertainment",
			"parent_number": "6220.000",
			"account_number": "6220.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Spoilage",
			"parent_number": "6220.000",
			"account_number": "6220.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Other Expenses",
			"parent_number": "6220.000",
			"account_number": "6220.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Laundry & Dry Cleaning Li",
			"parent_number": "6220.000",
			"account_number": "6220.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Laundry & Dry Cleaning Un",
			"parent_number": "6220.000",
			"account_number": "6220.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Utensil",
			"parent_number": "6220.000",
			"account_number": "6220.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Banquet Expense",
			"parent_number": "6220.000",
			"account_number": "6220.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Dues Subscription",
			"parent_number": "6220.000",
			"account_number": "6220.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "RESTO Exterm Desinfectan",
			"parent_number": "6220.000",
			"account_number": "6220.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6310.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Salaries & Wages",
			"parent_number": "6310.000",
			"account_number": "6310.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Jamsostek",
			"parent_number": "6310.000",
			"account_number": "6310.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Casual Worker",
			"parent_number": "6310.000",
			"account_number": "6310.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Bonus/THR",
			"parent_number": "6310.000",
			"account_number": "6310.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Employee Meals",
			"parent_number": "6310.000",
			"account_number": "6310.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Payroll Taxes & Benefits",
			"parent_number": "6310.000",
			"account_number": "6310.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Medical",
			"parent_number": "6310.000",
			"account_number": "6310.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Staff Transportation",
			"parent_number": "6310.000",
			"account_number": "6310.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Daily Worker Salary",
			"parent_number": "6310.000",
			"account_number": "6310.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN BPJS Kesehatan",
			"parent_number": "6310.000",
			"account_number": "6310.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6320.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN China,Glass,Silver",
			"parent_number": "6320.000",
			"account_number": "6320.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Linen",
			"parent_number": "6320.000",
			"account_number": "6320.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Cleaning Supplies",
			"parent_number": "6320.000",
			"account_number": "6320.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Guest Supplies",
			"parent_number": "6320.000",
			"account_number": "6320.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Paper Supplies",
			"parent_number": "6320.000",
			"account_number": "6320.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Uniforms",
			"parent_number": "6320.000",
			"account_number": "6320.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Decorations",
			"parent_number": "6320.000",
			"account_number": "6320.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Menus",
			"parent_number": "6320.000",
			"account_number": "6320.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Fuel",
			"parent_number": "6320.000",
			"account_number": "6320.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Supplies",
			"parent_number": "6320.000",
			"account_number": "6320.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Telephone",
			"parent_number": "6320.000",
			"account_number": "6320.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Contract Services",
			"parent_number": "6320.000",
			"account_number": "6320.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Entertainment",
			"parent_number": "6320.000",
			"account_number": "6320.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Transportation",
			"parent_number": "6320.000",
			"account_number": "6320.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Special Promotion",
			"parent_number": "6320.000",
			"account_number": "6320.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Postage / Express",
			"parent_number": "6320.000",
			"account_number": "6320.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Bar Supplies",
			"parent_number": "6320.000",
			"account_number": "6320.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Training",
			"parent_number": "6320.000",
			"account_number": "6320.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Equipment Rental",
			"parent_number": "6320.000",
			"account_number": "6320.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Licenses Fees",
			"parent_number": "6320.000",
			"account_number": "6320.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Printing & Stationary",
			"parent_number": "6320.000",
			"account_number": "6320.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Music & Entertainment",
			"parent_number": "6320.000",
			"account_number": "6320.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Spoilage",
			"parent_number": "6320.000",
			"account_number": "6320.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Other Expenses",
			"parent_number": "6320.000",
			"account_number": "6320.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Laundry & Dry Cleaning Li",
			"parent_number": "6320.000",
			"account_number": "6320.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Laundry & Dry Cleaning Un",
			"parent_number": "6320.000",
			"account_number": "6320.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Utensil",
			"parent_number": "6320.000",
			"account_number": "6320.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Banquet Expense",
			"parent_number": "6320.000",
			"account_number": "6320.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Dues Subscription",
			"parent_number": "6320.000",
			"account_number": "6320.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "KITCHEN Exterm Desinfectan",
			"parent_number": "6320.000",
			"account_number": "6320.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6410.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Salaries & Wages",
			"parent_number": "6410.000",
			"account_number": "6410.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Jamsostek",
			"parent_number": "6410.000",
			"account_number": "6410.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Casual Worker",
			"parent_number": "6410.000",
			"account_number": "6410.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Bonus/THR",
			"parent_number": "6410.000",
			"account_number": "6410.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Employee Meals",
			"parent_number": "6410.000",
			"account_number": "6410.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Payroll Taxes & Benefits",
			"parent_number": "6410.000",
			"account_number": "6410.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Medical",
			"parent_number": "6410.000",
			"account_number": "6410.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Staff Transportation",
			"parent_number": "6410.000",
			"account_number": "6410.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Daily Worker Salary",
			"parent_number": "6410.000",
			"account_number": "6410.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M BPJS Kesehatan",
			"parent_number": "6410.000",
			"account_number": "6410.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6420.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Uniforms",
			"parent_number": "6420.000",
			"account_number": "6420.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Systems Support",
			"parent_number": "6420.000",
			"account_number": "6420.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Telephone",
			"parent_number": "6420.000",
			"account_number": "6420.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Contract Services",
			"parent_number": "6420.000",
			"account_number": "6420.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Sales Call Outside",
			"parent_number": "6420.000",
			"account_number": "6420.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Transportation",
			"parent_number": "6420.000",
			"account_number": "6420.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M National Advertising Campaign",
			"parent_number": "6420.000",
			"account_number": "6420.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Postage / Express",
			"parent_number": "6420.000",
			"account_number": "6420.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Dues & Subscription",
			"parent_number": "6420.000",
			"account_number": "6420.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Training",
			"parent_number": "6420.000",
			"account_number": "6420.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Printing & Stationary",
			"parent_number": "6420.000",
			"account_number": "6420.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Other Expenses",
			"parent_number": "6420.000",
			"account_number": "6420.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Laundry & Dry Cleaning Uniform",
			"parent_number": "6420.000",
			"account_number": "6420.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Promotion",
			"parent_number": "6420.000",
			"account_number": "6420.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Entertaintment",
			"parent_number": "6420.000",
			"account_number": "6420.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Trade Show",
			"parent_number": "6420.000",
			"account_number": "6420.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Royalty & Marketing",
			"parent_number": "6420.000",
			"account_number": "6420.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Travelling Expenses",
			"parent_number": "6420.000",
			"account_number": "6420.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Adv Print Media Newspaper",
			"parent_number": "6420.000",
			"account_number": "6420.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Adv Rooms Electronic",
			"parent_number": "6420.000",
			"account_number": "6420.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Promotion VIP",
			"parent_number": "6420.000",
			"account_number": "6420.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Collateral Electronic",
			"parent_number": "6420.000",
			"account_number": "6420.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising F&B Print",
			"parent_number": "6420.000",
			"account_number": "6420.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising F&B Electroni",
			"parent_number": "6420.000",
			"account_number": "6420.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising F&B Outdoor",
			"parent_number": "6420.000",
			"account_number": "6420.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising Booking Engine",
			"parent_number": "6420.000",
			"account_number": "6420.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising Site Minder",
			"parent_number": "6420.000",
			"account_number": "6420.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising Revinate",
			"parent_number": "6420.000",
			"account_number": "6420.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Advertising Live Chat",
			"parent_number": "6420.000",
			"account_number": "6420.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Collateral Print",
			"parent_number": "6420.000",
			"account_number": "6420.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Collateral F&B Electronic",
			"parent_number": "6420.000",
			"account_number": "6420.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Giveaways Rooms",
			"parent_number": "6420.000",
			"account_number": "6420.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Giveaways F&B",
			"parent_number": "6420.000",
			"account_number": "6420.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Civic Community Project",
			"parent_number": "6420.000",
			"account_number": "6420.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Photography",
			"parent_number": "6420.000",
			"account_number": "6420.035",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Fee For Outside Service",
			"parent_number": "6420.000",
			"account_number": "6420.036",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Group Advertising Campaign",
			"parent_number": "6420.000",
			"account_number": "6420.037",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Fee",
			"parent_number": "6420.000",
			"account_number": "6420.038",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "S&M Kit",
			"parent_number": "6420.000",
			"account_number": "6420.039",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6510.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Salaries & Wages",
			"parent_number": "6510.000",
			"account_number": "6510.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Jamsostek",
			"parent_number": "6510.000",
			"account_number": "6510.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Casual Worker",
			"parent_number": "6510.000",
			"account_number": "6510.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Bonus/THR",
			"parent_number": "6510.000",
			"account_number": "6510.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Employee Meals",
			"parent_number": "6510.000",
			"account_number": "6510.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Payroll Taxes & Benefits",
			"parent_number": "6510.000",
			"account_number": "6510.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Medical",
			"parent_number": "6510.000",
			"account_number": "6510.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Staff Transportation/Relocation",
			"parent_number": "6510.000",
			"account_number": "6510.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Staff Housing",
			"parent_number": "6510.000",
			"account_number": "6510.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Daily Worker",
			"parent_number": "6510.000",
			"account_number": "6510.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC BPJS Kesehatan",
			"parent_number": "6510.000",
			"account_number": "6510.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6520.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Uniforms",
			"parent_number": "6520.000",
			"account_number": "6520.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Systems Support",
			"parent_number": "6520.000",
			"account_number": "6520.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Other Supplies",
			"parent_number": "6520.000",
			"account_number": "6520.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Telephone",
			"parent_number": "6520.000",
			"account_number": "6520.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Contract Services",
			"parent_number": "6520.000",
			"account_number": "6520.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Travel & Entertainment",
			"parent_number": "6520.000",
			"account_number": "6520.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Transportation",
			"parent_number": "6520.000",
			"account_number": "6520.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Other Professional Services",
			"parent_number": "6520.000",
			"account_number": "6520.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Postage / Express",
			"parent_number": "6520.000",
			"account_number": "6520.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Dues & Subscription",
			"parent_number": "6520.000",
			"account_number": "6520.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Training",
			"parent_number": "6520.000",
			"account_number": "6520.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Licenses & Fees",
			"parent_number": "6520.000",
			"account_number": "6520.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Printing & Stationary",
			"parent_number": "6520.000",
			"account_number": "6520.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Other Expenses",
			"parent_number": "6520.000",
			"account_number": "6520.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Laundry & Dry Cleaning Uniform",
			"parent_number": "6520.000",
			"account_number": "6520.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC IT Exp Software",
			"parent_number": "6520.000",
			"account_number": "6520.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC IT Exp Hardware",
			"parent_number": "6520.000",
			"account_number": "6520.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Credit Card Commissions",
			"parent_number": "6520.000",
			"account_number": "6520.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Credit & Collection Expense",
			"parent_number": "6520.000",
			"account_number": "6520.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC In House Intertainment",
			"parent_number": "6520.000",
			"account_number": "6520.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Legal Fees",
			"parent_number": "6520.000",
			"account_number": "6520.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Audit Fees",
			"parent_number": "6520.000",
			"account_number": "6520.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Accounting Fees",
			"parent_number": "6520.000",
			"account_number": "6520.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Donations",
			"parent_number": "6520.000",
			"account_number": "6520.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Recruitment",
			"parent_number": "6520.000",
			"account_number": "6520.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Bad Debt",
			"parent_number": "6520.000",
			"account_number": "6520.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Provision For Bad Debt.",
			"parent_number": "6520.000",
			"account_number": "6520.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Cashier Over/ Short",
			"parent_number": "6520.000",
			"account_number": "6520.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Bank Charges",
			"parent_number": "6520.000",
			"account_number": "6520.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Loss & Damages",
			"parent_number": "6520.000",
			"account_number": "6520.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Protective Services",
			"parent_number": "6520.000",
			"account_number": "6520.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Employee Relations",
			"parent_number": "6520.000",
			"account_number": "6520.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Difference Exchange Rate",
			"parent_number": "6520.000",
			"account_number": "6520.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "ACC Entertainment",
			"parent_number": "6520.000",
			"account_number": "6520.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6610.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Salaries & Wages",
			"parent_number": "6610.000",
			"account_number": "6610.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Jamsostek",
			"parent_number": "6610.000",
			"account_number": "6610.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Casual Worker",
			"parent_number": "6610.000",
			"account_number": "6610.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Bonus/THR",
			"parent_number": "6610.000",
			"account_number": "6610.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Employee Meals",
			"parent_number": "6610.000",
			"account_number": "6610.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Payroll Taxes & Benefits",
			"parent_number": "6610.000",
			"account_number": "6610.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Medical",
			"parent_number": "6610.000",
			"account_number": "6610.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Staff Transportation/Relocation",
			"parent_number": "6610.000",
			"account_number": "6610.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Daily Worker",
			"parent_number": "6610.000",
			"account_number": "6610.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD BPJS Kesehatan",
			"parent_number": "6610.000",
			"account_number": "6610.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6620.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Uniforms",
			"parent_number": "6620.000",
			"account_number": "6620.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Telephone",
			"parent_number": "6620.000",
			"account_number": "6620.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Contract Services",
			"parent_number": "6620.000",
			"account_number": "6620.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Transportation",
			"parent_number": "6620.000",
			"account_number": "6620.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Postage / Express",
			"parent_number": "6620.000",
			"account_number": "6620.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Dues & Subscription",
			"parent_number": "6620.000",
			"account_number": "6620.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Training",
			"parent_number": "6620.000",
			"account_number": "6620.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Printing & Stationary",
			"parent_number": "6620.000",
			"account_number": "6620.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Other Expenses",
			"parent_number": "6620.000",
			"account_number": "6620.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Laundry & Dry Cleaning Uniform",
			"parent_number": "6620.000",
			"account_number": "6620.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Photography",
			"parent_number": "6620.000",
			"account_number": "6620.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Advertising",
			"parent_number": "6620.000",
			"account_number": "6620.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Recruitment",
			"parent_number": "6620.000",
			"account_number": "6620.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Donations",
			"parent_number": "6620.000",
			"account_number": "6620.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Sport & Social Activity",
			"parent_number": "6620.000",
			"account_number": "6620.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Employee Relation",
			"parent_number": "6620.000",
			"account_number": "6620.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Loss & Damage",
			"parent_number": "6620.000",
			"account_number": "6620.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Outsource Expenses",
			"parent_number": "6620.000",
			"account_number": "6620.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Entertainment",
			"parent_number": "6620.000",
			"account_number": "6620.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD License",
			"parent_number": "6620.000",
			"account_number": "6620.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "HRD Ceremonies",
			"parent_number": "6620.000",
			"account_number": "6620.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6710.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Salaries & Wages",
			"parent_number": "6710.000",
			"account_number": "6710.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Jamsostek",
			"parent_number": "6710.000",
			"account_number": "6710.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Casual Worker",
			"parent_number": "6710.000",
			"account_number": "6710.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Bonus/THR",
			"parent_number": "6710.000",
			"account_number": "6710.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Employee Meals",
			"parent_number": "6710.000",
			"account_number": "6710.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Payroll Taxes & Benefits",
			"parent_number": "6710.000",
			"account_number": "6710.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Medical",
			"parent_number": "6710.000",
			"account_number": "6710.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Staff Transportation/Relocation",
			"parent_number": "6710.000",
			"account_number": "6710.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Daily Worker",
			"parent_number": "6710.000",
			"account_number": "6710.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security BPJS Kesehatan",
			"parent_number": "6710.000",
			"account_number": "6710.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Security Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6720.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6810.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Salaries & Wages",
			"parent_number": "6810.000",
			"account_number": "6810.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Jamsostek",
			"parent_number": "6810.000",
			"account_number": "6810.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Casual Worker",
			"parent_number": "6810.000",
			"account_number": "6810.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Bonus/THR",
			"parent_number": "6810.000",
			"account_number": "6810.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Employee Meals",
			"parent_number": "6810.000",
			"account_number": "6810.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Payroll Taxes & Benefits",
			"parent_number": "6810.000",
			"account_number": "6810.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Medical",
			"parent_number": "6810.000",
			"account_number": "6810.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Staff Transportation/Relocation",
			"parent_number": "6810.000",
			"account_number": "6810.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Daily Worker",
			"parent_number": "6810.000",
			"account_number": "6810.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering BPJS Kesehatan",
			"parent_number": "6810.000",
			"account_number": "6810.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Other Expenses",
			"parent_number": "6000.000",
			"account_number": "6820.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Uniforms",
			"parent_number": "6820.000",
			"account_number": "6820.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Other Supplies",
			"parent_number": "6820.000",
			"account_number": "6820.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Postage/Express",
			"parent_number": "6820.000",
			"account_number": "6820.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Contract Services",
			"parent_number": "6820.000",
			"account_number": "6820.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Transportation",
			"parent_number": "6820.000",
			"account_number": "6820.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Telephone and Fax",
			"parent_number": "6820.000",
			"account_number": "6820.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Due Subcription",
			"parent_number": "6820.000",
			"account_number": "6820.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Printing & Stationary",
			"parent_number": "6820.000",
			"account_number": "6820.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Other Expenses",
			"parent_number": "6820.000",
			"account_number": "6820.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Laundry & Dry Cleaning Uniform",
			"parent_number": "6820.000",
			"account_number": "6820.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Cleaning Supplies",
			"parent_number": "6820.000",
			"account_number": "6820.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Entertainment",
			"parent_number": "6820.000",
			"account_number": "6820.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Aircon & Ventilation",
			"parent_number": "6820.000",
			"account_number": "6820.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Building",
			"parent_number": "6820.000",
			"account_number": "6820.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Audio Visual And Sound System",
			"parent_number": "6820.000",
			"account_number": "6820.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Electrical",
			"parent_number": "6820.000",
			"account_number": "6820.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Electric Bulbs",
			"parent_number": "6820.000",
			"account_number": "6820.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Elev & Escalators",
			"parent_number": "6820.000",
			"account_number": "6820.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Floor Covering",
			"parent_number": "6820.000",
			"account_number": "6820.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Furniture",
			"parent_number": "6820.000",
			"account_number": "6820.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Grounds & L&scape",
			"parent_number": "6820.000",
			"account_number": "6820.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering F&B Kithcen & Refrig",
			"parent_number": "6820.000",
			"account_number": "6820.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Laundry",
			"parent_number": "6820.000",
			"account_number": "6820.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Mechanical",
			"parent_number": "6820.000",
			"account_number": "6820.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Vehicle Maintenance",
			"parent_number": "6820.000",
			"account_number": "6820.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Painting & Decoration",
			"parent_number": "6820.000",
			"account_number": "6820.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Plumbing & Heating",
			"parent_number": "6820.000",
			"account_number": "6820.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Recreation Facilities",
			"parent_number": "6820.000",
			"account_number": "6820.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Genset",
			"parent_number": "6820.000",
			"account_number": "6820.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Gondola",
			"parent_number": "6820.000",
			"account_number": "6820.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Office Equipment",
			"parent_number": "6820.000",
			"account_number": "6820.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Removal of Waste Matter",
			"parent_number": "6820.000",
			"account_number": "6820.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Life Safety",
			"parent_number": "6820.000",
			"account_number": "6820.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Locks & Keys",
			"parent_number": "6820.000",
			"account_number": "6820.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Water Treatment",
			"parent_number": "6820.000",
			"account_number": "6820.035",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering STP",
			"parent_number": "6820.000",
			"account_number": "6820.036",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Payroll and Related",
			"parent_number": "6000.000",
			"account_number": "6910.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Salaries & Wages",
			"parent_number": "6910.000",
			"account_number": "6910.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Jamsostek",
			"parent_number": "6910.000",
			"account_number": "6910.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Casual Worker",
			"parent_number": "6910.000",
			"account_number": "6910.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Bonus/THR",
			"parent_number": "6910.000",
			"account_number": "6910.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Employee Meals",
			"parent_number": "6910.000",
			"account_number": "6910.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Payroll Taxes & Benefits",
			"parent_number": "6910.000",
			"account_number": "6910.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Medical",
			"parent_number": "6910.000",
			"account_number": "6910.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate Staff Transportation/Relocation",
			"parent_number": "6910.000",
			"account_number": "6910.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Corporate BPJS Kesehatan",
			"parent_number": "6910.000",
			"account_number": "6910.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Energy Cost",
			"parent_number": "6000.000",
			"account_number": "6830.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Electricity",
			"parent_number": "6830.000",
			"account_number": "6830.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Boiler Fuel",
			"parent_number": "6830.000",
			"account_number": "6830.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Diesel Fuel",
			"parent_number": "6830.000",
			"account_number": "6830.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Steam",
			"parent_number": "6830.000",
			"account_number": "6830.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Water & Sewage",
			"parent_number": "6830.000",
			"account_number": "6830.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Expense",
			"parent_number": "",
			"account_number": "7000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Operational Supplies",
			"parent_number": "7000.000",
			"account_number": "7100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Paper Supplies",
			"parent_number": "7100.000",
			"account_number": "7101.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Print and Stationary",
			"parent_number": "7100.000",
			"account_number": "7102.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Office Supplies",
			"parent_number": "7100.000",
			"account_number": "7103.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Cleaning Supplies",
			"parent_number": "7100.000",
			"account_number": "7104.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Gas",
			"parent_number": "7100.000",
			"account_number": "7105.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "FB Supplies",
			"parent_number": "7100.000",
			"account_number": "7106.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Room Supplies",
			"parent_number": "7100.000",
			"account_number": "7107.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Sales & Marketing Supplies",
			"parent_number": "7100.000",
			"account_number": "7108.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Supplies",
			"parent_number": "7100.000",
			"account_number": "7109.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Electric Bulb Supplies",
			"parent_number": "7100.000",
			"account_number": "7110.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Building and Office Expense",
			"parent_number": "7000.000",
			"account_number": "7200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Electricity",
			"parent_number": "7200.000",
			"account_number": "7201.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Water and Sewage",
			"parent_number": "7200.000",
			"account_number": "7202.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Telephone",
			"parent_number": "7200.000",
			"account_number": "7203.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Internet",
			"parent_number": "7200.000",
			"account_number": "7204.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "TV Cable & Satellite",
			"parent_number": "7200.000",
			"account_number": "7205.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Pest Control",
			"parent_number": "7200.000",
			"account_number": "7206.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Air Conditioning",
			"parent_number": "7200.000",
			"account_number": "7207.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Elevator and Escalator",
			"parent_number": "7200.000",
			"account_number": "7208.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Furniture",
			"parent_number": "7200.000",
			"account_number": "7209.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Garbage Cleaning",
			"parent_number": "7200.000",
			"account_number": "7210.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Cleaning Equipment",
			"parent_number": "7200.000",
			"account_number": "7211.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Building Maintenance",
			"parent_number": "7200.000",
			"account_number": "7212.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Engineering Equipment",
			"parent_number": "7200.000",
			"account_number": "7213.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Other Building and Office Expense",
			"parent_number": "7200.000",
			"account_number": "7214.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Audio Visual and Sound System",
			"parent_number": "7200.000",
			"account_number": "7215.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Room/Bathroom Equipment",
			"parent_number": "7200.000",
			"account_number": "7216.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Mechanical and Electrical Equipment",
			"parent_number": "7200.000",
			"account_number": "7217.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "General Expense",
			"parent_number": "7000.000",
			"account_number": "7300.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Fuel",
			"parent_number": "7300.000",
			"account_number": "7301.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Parking",
			"parent_number": "7300.000",
			"account_number": "7302.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Transportation",
			"parent_number": "7300.000",
			"account_number": "7303.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Postage",
			"parent_number": "7300.000",
			"account_number": "7304.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Vehicle Repair Expense",
			"parent_number": "7300.000",
			"account_number": "7305.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Stock Adjustment",
			"parent_number": "7300.000",
			"account_number": "7306.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock Adjustment",
			"root_type": "Expense"
		},
		{
			"account_name": "China, Glassware, Silver, Linen Expense",
			"parent_number": "7000.000",
			"account_number": "7400.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "China Expense",
			"parent_number": "7400.000",
			"account_number": "7401.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Glassware Expense",
			"parent_number": "7400.000",
			"account_number": "7402.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Silver Expense",
			"parent_number": "7400.000",
			"account_number": "7403.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Linen Expense",
			"parent_number": "7400.000",
			"account_number": "7404.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Information System Expense",
			"parent_number": "7000.000",
			"account_number": "7500.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Hardware Expense",
			"parent_number": "7500.000",
			"account_number": "7501.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Software Expense",
			"parent_number": "7500.000",
			"account_number": "7502.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "IT Consultant Expense",
			"parent_number": "7500.000",
			"account_number": "7503.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Other Information System Expense",
			"parent_number": "7500.000",
			"account_number": "7504.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Other Expense",
			"parent_number": "7000.000",
			"account_number": "7600.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		},
		{
			"account_name": "Administration Bank",
			"parent_number": "7600.000",
			"account_number": "7601.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account",
			"root_type": "Expense"
		},
		{
			"account_name": "Land and Building Tax (PBB)",
			"parent_number": "7600.000",
			"account_number": "7602.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax",
			"root_type": "Expense"
		},
		{
			"account_name": "Income Tax",
			"parent_number": "7600.000",
			"account_number": "7603.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax",
			"root_type": "Expense"
		},
		{
			"account_name": "PPN Tax",
			"parent_number": "7600.000",
			"account_number": "7604.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax",
			"root_type": "Expense"
		},
		{
			"account_name": "Depreciation",
			"parent_number": "7600.000",
			"account_number": "7605.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Depreciation",
			"root_type": "Expense"
		},
		{
			"account_name": "Round Off",
			"parent_number": "7600.000",
			"account_number": "7607.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Round Off",
			"root_type": "Expense"
		},
		{
			"account_name": "Write Off",
			"parent_number": "7600.000",
			"account_number": "7608.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "",
			"root_type": "Expense"
		}
	]
	return accounts
