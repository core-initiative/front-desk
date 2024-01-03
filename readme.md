### Notes

1. Child table untuk menyambung antara Menu Item dengan Menu

   > Menu Item tidak bisa dijadikan child table karena perlu diakses oleh Ongoing Order dan Finished Order.
   > Sehingga perlu dibuat child table baru untuk menyambung antara kedua doctype.

2. Child table untuk menyambung dari Restaurant ke Restaurant Table _(Opsional)_

   > Restaurant Table tidak bisa dijadikan child table karena perlu diakses oleh Ongoing Order dan Finised Order.
   > Ini menjadi opsional karena Restaurant bisa saja tidak perlu memiliki entitas Table di dalam detail Restaurant.

3. Menghubungan antara Customer dengan Supplier
   > Setiap hotel customer butuh menjadi entitas supplier. Hal ini disebabkan Guest Deposit bertipe sebagai "Payable" sementara entitas Customer adalah pihak ke-3 yang bertipe "Receivable".
   >
   > Untuk setiap pembuatan Customer baru perlu diiringi dengan pembuatan entitas Supplier dengan nama yang sama persis.
   >
   > Apabila perlu dihubungkan maka dapat di aktifkan Common Party Accounting ERPNext. (Account Settings > Common Party Accounting) _(Opsional)_
