#Python program to convert retrieve your contacts from an android backup
#Make sure to run it in the same folder as contacts2.db
#Libraries needed : sqlite3

import sqlite3

CONTACTS = "contacts2.db"

conn = sqlite3.connect(CONTACTS)
cursor = conn.cursor()

try:
    cursor.execute('''SELECT raw_contacts._id, raw_contacts.display_name, raw_contacts.display_name_alt, mimetypes.mimetype, REPLACE(REPLACE(data.data1, '\r\n', '\n'), '\n', '\n'), data.data2, REPLACE(REPLACE(data.data4, '\r\n', '\n'), '\n', '\n'), data.data5, data.data6, data.data7, data.data8, data.data9, data.data10, quote(data.data15) FROM raw_contacts, data, mimetypes WHERE raw_contacts.deleted = 0 AND raw_contacts._id = data.raw_contact_id AND data.mimetype_id = mimetypes._id ORDER BY raw_contacts._id, mimetypes._id, data.data2''')

    prev_contact_id = 0
    cur_vcard = ""

    for row in cursor.fetchall():
        cur_contact_id, cur_display_name, cur_display_name_alt, cur_mimetype, cur_data1, cur_data2, cur_data4, cur_data5, cur_data6, cur_data7, cur_data8, cur_data9, cur_data10, cur_data15 = row

        if prev_contact_id != cur_contact_id:
            if prev_contact_id != 0:
                cur_vcard += "END:VCARD\n"
                print(cur_vcard)

            cur_vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{cur_display_name_alt}\nFN:{cur_display_name}\n"
            prev_contact_id = cur_contact_id

        if cur_mimetype == "vnd.android.cursor.item/nickname":
            if cur_data1:
                cur_vcard += f"NICKNAME:{cur_data1}\n"
        elif cur_mimetype == "vnd.android.cursor.item/organization":
            if cur_data1:
                cur_vcard += f"ORG:{cur_data1}\n"
            if cur_data4:
                cur_vcard += f"TITLE:{cur_data4}\n"
        elif cur_mimetype == "vnd.android.cursor.item/phone_v2":
            if cur_data1 and cur_data2:
                phone_type = "CELL,VOICE,PREF" if cur_data2 == "2" else "HOME" if cur_data2 == "1" else "WORK"
                cur_vcard += f"TEL;TYPE={phone_type}:{cur_data1}\n"

    cur_vcard += "END:VCARD\n"

    with open("contacts2.vcf", "w") as file:
        file.write(cur_vcard)
    print("vCard data written to contacts2.vcf")

except sqlite3.Error as e:
    print("Error executing SQLite query:", e)

conn.close()
