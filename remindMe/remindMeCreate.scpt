JsOsaDAS1.001.00bplist00�Vscript_�// Access command-line arguments
var args = $.NSProcessInfo.processInfo.arguments; // Use Objective-C bridge to get arguments
var argv = []; // Array to hold converted arguments
for (var i = 4; i < args.count; i++) { // Start at 4 to skip the first few default args
    argv.push(ObjC.unwrap(args.objectAtIndex(i)));
}

// Arguments passed from command line
var reminderTitle = argv[0]; // First argument: Title of the reminder
var listName = argv[1]; // Second argument: The name of the list
var dueDateString = argv[2]; // Third argument: Due date as string

// Convert due date string to Date object
var dueDate = new Date(dueDateString);

// Rest of the script remains the same
var RemindersApp = Application('Reminders');
var targetList = RemindersApp.lists.whose({name: listName})[0];
var newReminder = RemindersApp.Reminder({name: reminderTitle, dueDate: dueDate});
targetList.reminders.push(newReminder);
console.log("Created a new reminder with title '" + reminderTitle + "' due on " + dueDate);
                               jscr  
��ޭ