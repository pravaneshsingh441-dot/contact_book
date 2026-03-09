# Contact Book

A user-friendly desktop application for managing your contacts efficiently.

## Features

✨ **Contact Management:**
- **Add Contact**: Create new contacts with name, phone, email, and address
- **View Contact List**: Display all saved contacts in an organized table
- **Search Contact**: Find contacts by name or phone number
- **Update Contact**: Modify existing contact details (double-click or use Edit button)
- **Delete Contact**: Remove contacts (right-click or use Delete button)

## User Interface

The application provides:
- Clean, intuitive GUI built with Python tkinter
- Color-coded buttons for easy navigation
- Searchable contact list
- Right-click context menu for quick actions
- Status bar showing total number of contacts

## Installation

### Requirements:
- Python 3.x
- tkinter (included with Python)

### Setup:
1. Python comes with tkinter pre-installed, so no additional installation is needed

## Usage

Run the application:
```bash
python contact_book.py
```

### How to Use:

1. **Add Contact**: Click the "➕ Add Contact" button, fill in the details, and click Save
2. **View Contacts**: All contacts are displayed in the table automatically
3. **Search**: Click the "🔍 Search" button and enter a name or phone number
4. **Edit Contact**: Double-click a contact or click "✏️ Edit Selected"
5. **Delete Contact**: Right-click a contact or click "🗑️ Delete Selected"
6. **Refresh**: Click the "🔄 Refresh" button to reload the contact list

## Data Storage

Contacts are automatically saved to a `contacts.json` file in the same directory as the application.

## Features in Detail

### Add Contact Page
- Enter Contact Name (required)
- Enter Phone Number (required)
- Optional: Email and Address
- Click "Save Contact" to store

### Search Functionality
- Search by partial or full name
- Search by phone number
- Results displayed in the main table

### Edit/Update Contact
- Double-click any contact OR select and click "✏️ Edit Selected"
- Modify name, email, or address (phone cannot be changed)
- Click "Update Contact" to save changes

### Delete Contact
- Right-click any contact and select "Delete"
- OR select and click "🗑️ Delete Selected"
- Confirm deletion in the prompt

## Technical Details

- **Language**: Python 3
- **GUI Framework**: tkinter (built-in)
- **Data Format**: JSON
- **File Storage**: contacts.json

## Notes

- Phone numbers are used as unique identifiers
- All contacts persist between sessions
- Entries are sorted alphabetically by name in the list
- The application creates/updates the contacts.json file automatically
## Author
Pravanesh singh