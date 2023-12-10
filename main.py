from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import os
from typing import Tuple, Optional
import shlex 

# Define states for the conversation
CHOOSING_ACTION = range(1)
BUY_CONSULT_NAME, BUY_CONSULT_PHONE, BUY_CONSULT_EMAIL, BUY_CONSULT_DEGREE, BUY_CONSULT_FIELD, BUY_CONSULT_AGE, BUY_CONSULT_DESIRED_FIELD, BUY_CONSULT_BANK_RECEIPT = range(8)
RESUME_NAME, RESUME_AGE, RESUME_UNIVERSITY, RESUME_MAJOR, RESUME_GPA, RESUME_DESIRED_MAJOR, RESUME_DESIRED_UNIVERSITY, RESUME_STUDY_DURATION, RESUME_PROJECTS, RESUME_SKILLS, RESUME_WORK_EXPERIENCE, RESUME_STUDY_PURPOSE, RESUME_PHOTO, RESUME_RECOMMENDATIONS, RESUME_EMAIL, RESUME_BIRTH_DATE, RESUME_LANGUAGE_SKILLS, RESUME_LAST_UNIVERSITY_PROJECT, RESUME_PROJECT_GPA, RESUME_HOBBIES, RESUME_INTERESTING_COURSES, BANK_RECEIPT, PHONE_NUMBER  = range(23)
# Unique states for the "فرم انگیزه نامه" conversation
MOTIVATION_NAME, MOTIVATION_AGE, MOTIVATION_PHONE, MOTIVATION_UNIVERSITY, MOTIVATION_MAJOR, MOTIVATION_GPA, MOTIVATION_DESIRED_MAJOR, MOTIVATION_DESIRED_UNIVERSITY, MOTIVATION_PROJECTS, MOTIVATION_SKILLS, MOTIVATION_WORK_EXPERIENCE, MOTIVATION_STUDY_PURPOSE, MOTIVATION_BANK_RECEIPT = range(13)
RECOMMENDATION_NAME, RECOMMENDATION_PHONE, RECOMMENDATION_UNIVERSITY, RECOMMENDATION_MAJOR, RECOMMENDATION_DESIRED_UNIVERSITY, RECOMMENDATION_PROFESSOR_NAME, RECOMMENDATION_COURSE_NAME, RECOMMENDATION_COURSE_GRADE, RECOMMENDATION_BANK_RECEIPT = range(9)
VIP_FAMILY_NAME, VIP_STUDENT_PHONE, VIP_STUDENT_MAJOR, VIP_STUDENT_GPA, VIP_STUDENT_BANK_RECEIPT = range(5)


# Map user_id to admin_id for sending pictures
admin_user_id = #<admin-user-id>



def get_telegram_username(user):
    return user.username if user.username else "N/A"

# Function to handle the /cancel command outside the conversation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Canceled.")
    start(update, context)
    return ConversationHandler.END
# Callback query handler for inline keyboard buttons
def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Split the callback data
    _, chat_id = query.data.split(' ')

    # Prepare the message with a pre-filled command
    message_with_command = f'/send {chat_id} " "'
    context.bot.send_message(chat_id=query.from_user.id, text=message_with_command)

def convert_farsi_numerals(input_string):
    # Dictionary to map Farsi numerals to Latin numerals
    farsi_to_latin = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }

    # Check if the input string contains Farsi numerals
    if any(char in farsi_to_latin for char in input_string):
        # Replace Farsi numerals with Latin numerals
        converted_string = ''.join(farsi_to_latin.get(char, char) for char in input_string)
        return converted_string
    else:
        # No Farsi numerals found, return the original string
        return input_string

# Send command handler function
def send_command(update: Update, context: CallbackContext) -> None:
    # Verify if the user is an admin
    if update.effective_user.id != admin_user_id:
        update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        # Parse arguments using shlex to keep the integrity of quoted messages
        args = shlex.split(update.message.text)[1:]  # Skip the command '/send'

        # Check if we have at least two arguments (chat_id and message)
        if len(args) >= 2:
            chat_id = args[0]
            message = " ".join(args[1:])  # Join the message parts preserving newlines

            # Send the message
            context.bot.send_message(chat_id=chat_id, text=message)
            update.message.reply_text(f"Message sent to chat ID {chat_id}.")
        else:
            update.message.reply_text("Usage: /send <chat_id> <message>")
    except IndexError as ie:
        update.message.reply_text("Usage: /send <chat_id> <message>")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")



# Handler to start the chat and provide options
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "خوش آمدید! یک گزینه را انتخاب کنید، در صورت انتخاب گزینه اشتباه فرمان /cancel را تایپ کنید.",
        reply_markup={"keyboard": [["خرید مشاوره"], ["فرم رزومه"], ["فرم انگیزه نامه"], ["فرم توصیه نامه"],["AskApply"]], "one_time_keyboard": True},
    )
    return CHOOSING_ACTION 

##############################BUY CONSULT############################################
# Function to start the buy consult form
def start_buy_consult(update: Update, context: CallbackContext) -> int:
    
    update.message.reply_text("لطفاً نام و نام خانوادگی خود را وارد کنید:",reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Clear user_data to start with a clean slate
    return BUY_CONSULT_NAME

# Function to collect the name
def collect_buy_consult_name(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_name"] = update.message.text

    user_chat_id = update.message.chat_id  # Get the user's chat ID
    user_id = update.message.from_user.id  # Get the user's ID
    context.user_data[user_id] = {"user_chat_id": user_chat_id,
                                   "name": context.user_data.get("buy_consult_name", "N/A")}

    # Provide a prompt for the next step
    update.message.reply_text("لطفا شماره موبایل متصل به تلگرام خود را وارد کنید:")

    # Return the next state
    return BUY_CONSULT_PHONE

# Function to collect the phone number
def collect_buy_consult_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_phone"] = update.message.text
    update.message.reply_text("لطفاً آدرس ایمیل خود را وارد کنید:")
    return BUY_CONSULT_EMAIL

# Handler for collecting user's email address
def collect_buy_consult_email(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_email"] = update.message.text
    update.message.reply_text("لطفاً مقطع تحصیلی خود را وارد کنید:")
    return BUY_CONSULT_DEGREE

# Function to collect the degree
def collect_buy_consult_degree(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_degree"] = update.message.text
    update.message.reply_text("لطفاً رشته تحصیلی خود را وارد کنید:")
    return BUY_CONSULT_FIELD

# Function to collect the field of study
def collect_buy_consult_field(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_field"] = update.message.text
    update.message.reply_text("لطفاً سن خود را وارد کنید:")
    return BUY_CONSULT_AGE

# Function to collect the age
def collect_buy_consult_age(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_age"] = update.message.text
    update.message.reply_text("لطفاً رشته مورد نظر خود را بنویسید:")
    return BUY_CONSULT_DESIRED_FIELD

# Function to collect the desired field of study
def collect_buy_consult_desired_field(update: Update, context: CallbackContext) -> int:
    context.user_data["buy_consult_desired_field"] = update.message.text
    update.message.reply_text("")
    return BUY_CONSULT_BANK_RECEIPT

# Function to collect the bank receipt
def collect_buy_consult_bank_receipt(update: Update, context: CallbackContext) -> int:
    # Save the photo of the bank receipt for further processing
    image_directory = "images/buy_consult_bank_receipts/"
    os.makedirs(image_directory, exist_ok=True)
    image_path = image_directory + f"{update.message.from_user.id}_buy_consult_bank_receipt.jpg"
    update.message.photo[-1].get_file().download(image_path)
    
    # Update user_data with the bank receipt photo path
    context.user_data["buy_consult_bank_receipt"] = image_path

    # Get user information
    buy_consult_name = context.user_data.get("buy_consult_name", "N/A")
    buy_consult_phone = context.user_data.get("buy_consult_phone", "N/A")
    buy_consult_email = context.user_data.get("buy_consult_email", "N/A")
    buy_consult_degree = context.user_data.get("buy_consult_degree", "N/A")
    buy_consult_field = context.user_data.get("buy_consult_field", "N/A")
    buy_consult_age = context.user_data.get("buy_consult_age", "N/A")
    buy_consult_desired_field = context.user_data.get("buy_consult_desired_field", "N/A")
    buy_consult_bank_receipt = context.user_data.get("buy_consult_bank_receipt", "N/A")
    user_phone_formatted = f"+98{buy_consult_phone[1:]}"
    # Create a link to the user's ID
    user_id_link = f"https://t.me/{convert_farsi_numerals(user_phone_formatted)}"

    user_chat_id = update.effective_message.chat_id
    # Prepare the callback data for the button
    callback_data = f"send {user_chat_id}"
    # Create the inline keyboard markup
    keyboard = [[InlineKeyboardButton(text="Reply to this user", callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Forward the image and user information to the admin
    message_text = f"خرید مشاوره\nBuy Consult form details received from user:\nName: {buy_consult_name}\nPhone: {buy_consult_phone}\nEmail: {buy_consult_email}\nDegree: {buy_consult_degree}\nField: {buy_consult_field}\nAge: {buy_consult_age}\nDesired Field: {buy_consult_desired_field}\nUser_link: {user_id_link}"

    # Send the message without inline keyboard
    context.bot.send_message(chat_id=admin_user_id, text=message_text, reply_markup=reply_markup)
    context.bot.send_photo(chat_id=admin_user_id, photo=open(image_path, "rb"))
    
    update.message.reply_text("اطلاعات شما با موفقیت ثبت شد. با تشکر!")
    start(update, context)
    return ConversationHandler.END


###################################### فرم رزومه#########################################

def start_resume_form(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لطفاً نام و نام خانوادگی خود را وارد کنید:",
        reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Clear user_data to start with a clean slate
    return RESUME_NAME

def collect_resume_name(update: Update, context: CallbackContext) -> int:
    context.user_data["name"] = update.message.text
    context.user_data["telegram_username"] = get_telegram_username(update.message.from_user)
    update.message.reply_text("لطفاً سن خود را وارد کنید:")
    return RESUME_AGE

def collect_age(update: Update, context: CallbackContext) -> int:
    context.user_data["age"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه محل تحصیل خود را وارد کنید:")
    return RESUME_UNIVERSITY

def collect_university(update: Update, context: CallbackContext) -> int:
    context.user_data["university"] = update.message.text
    update.message.reply_text("لطفاً رشته محل تحصیل خود را وارد کنید:")
    return RESUME_MAJOR
    
def collect_major(update: Update, context: CallbackContext) -> int:
    context.user_data["major"] = update.message.text
    update.message.reply_text("لطفاً معدل خود را وارد کنید:")
    return RESUME_GPA

def collect_gpa(update: Update, context: CallbackContext) -> int:
    context.user_data["gpa"] = update.message.text
    update.message.reply_text("لطفاً رشته مورد نظر خود را وارد کنید:")
    return RESUME_DESIRED_MAJOR

def collect_desired_major(update: Update, context: CallbackContext) -> int:
    context.user_data["desired_major"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه مورد نظر خود را وارد کنید:")
    return RESUME_DESIRED_UNIVERSITY

def collect_desired_university(update: Update, context: CallbackContext) -> int:
    context.user_data["desired_university"] = update.message.text
    update.message.reply_text("از چه سالی تا چه سالی لیسانس طول کشیده؟")
    return RESUME_STUDY_DURATION

def collect_study_duration(update: Update, context: CallbackContext) -> int:
    context.user_data["study_duration"] = update.message.text
    update.message.reply_text("پروژه و تحقیقاتی که طی دوران تحصیل انجام داده‌اید را بنویسید:")
    return RESUME_PROJECTS

def collect_projects(update: Update, context: CallbackContext) -> int:
    context.user_data["projects"] = update.message.text
    update.message.reply_text("لطفاً مهارت‌های خود را بنویسید:")
    return RESUME_SKILLS

def collect_skills(update: Update, context: CallbackContext) -> int:
    context.user_data["skills"] = update.message.text
    update.message.reply_text("سابقه کار خود را اگر دارید بنویسید:")
    return RESUME_WORK_EXPERIENCE

def collect_work_experience(update: Update, context: CallbackContext) -> int:
    context.user_data["work_experience"] = update.message.text
    update.message.reply_text("هدف شما از خواندن این رشته چیست؟")
    return RESUME_STUDY_PURPOSE

def collect_study_purpose(update: Update, context: CallbackContext) -> int:
    context.user_data["study_purpose"] = update.message.text
    update.message.reply_text("لطفاً یک عکس سه در چهار بفرستید:")
    return RESUME_PHOTO

def collect_photo(update: Update, context: CallbackContext) -> int:
    # Save the photo for further processing
    photo_path = "images/applicant_photos/"
    os.makedirs(photo_path, exist_ok=True)
    photo_filename = f"{update.message.from_user.id}_photo.jpg"
    photo_file_path = os.path.join(photo_path, photo_filename)
    update.message.photo[-1].get_file().download(photo_file_path)

    # Update user_data with photo path
    context.user_data["photo"] = photo_file_path

    # Continue with the next step or conclude the form
    update.message.reply_text("نام دو استاد برای ریکامندیشن و ایمیلشان را بنویسید:")
    return RESUME_RECOMMENDATIONS

def collect_recommendations(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendations"] = update.message.text
    update.message.reply_text("ایمیل خود را وارد کنید:")
    return RESUME_EMAIL

def collect_email_resume(update: Update, context: CallbackContext) -> int:
    context.user_data["email"] = update.message.text
    update.message.reply_text("تاریخ تولد خود را وارد کنید:")
    return RESUME_BIRTH_DATE

def collect_birth_date(update: Update, context: CallbackContext) -> int:
    context.user_data["birth_date"] = update.message.text
    update.message.reply_text("سطح زبان انگلیسی و هر زبان دیگری که بلدید را بنویسید:")
    return RESUME_LANGUAGE_SKILLS

def collect_language_skills(update: Update, context: CallbackContext) -> int:
    context.user_data["language_skills"] = update.message.text
    update.message.reply_text("آخرین پروژه‌ای که در دانشگاه انجام دادید را بنویسید:")
    return RESUME_LAST_UNIVERSITY_PROJECT

def collect_last_university_project(update: Update, context: CallbackContext) -> int:
    context.user_data["last_university_project"] = update.message.text
    update.message.reply_text("معدل پروژه را وارد کنید:")
    return RESUME_PROJECT_GPA

def collect_project_gpa(update: Update, context: CallbackContext) -> int:
    context.user_data["project_gpa"] = update.message.text
    update.message.reply_text("علایق شخصی و سرگرمی‌هایتان چیست؟")
    return RESUME_HOBBIES

def collect_hobbies(update: Update, context: CallbackContext) -> int:
    context.user_data["hobbies"] = update.message.text
    update.message.reply_text("درس‌های تخصصی که در طول دوره تحصیل خود خوب بوده‌اید را بنویسید:")
    return RESUME_INTERESTING_COURSES

def collect_interesting_courses(update: Update, context: CallbackContext) -> int:
    context.user_data["interesting_courses"] = update.message.text

    # Request the phone number
    update.message.reply_text("لطفا شماره موبایل متصل به تلگرام خود را وارد کنید:")

    # Move to the next state
    return PHONE_NUMBER

def collect_phone_number(update: Update, context: CallbackContext) -> int:
    context.user_data["phone_number"] = update.message.text
    update.message.reply_text("")
    return BANK_RECEIPT

def collect_bank_receipt(update: Update, context: CallbackContext) -> int:
    # Save the image for further processing
    image_directory = "images/payment_pictures/"
    os.makedirs(image_directory, exist_ok=True)

    # Construct the full path for the image
    image_path = image_directory + "payment_image.jpg"
    update.message.photo[-1].get_file().download(image_path)

    # Extract relevant information from user_data
    user_name = context.user_data.get("name", "N/A")
    user_phone = context.user_data.get("phone_number", "N/A")
    user_email = context.user_data.get("email", "N/A")
    telegram_username = context.user_data.get("telegram_username", "N/A")
    photo_path = context.user_data.get("photo", "N/A")
    age = context.user_data.get("age", "N/A")
    university = context.user_data.get("university", "N/A")
    major = context.user_data.get("major", "N/A")
    gpa = context.user_data.get("gpa", "N/A")
    desired_major = context.user_data.get("desired_major", "N/A")
    desired_university = context.user_data.get("desired_university", "N/A")
    study_duration = context.user_data.get("study_duration", "N/A")
    projects = context.user_data.get("projects", "N/A")
    skills = context.user_data.get("skills", "N/A")
    work_experience = context.user_data.get("work_experience", "N/A")
    study_purpose = context.user_data.get("study_purpose", "N/A")
    birth_date = context.user_data.get("birth_date", "N/A")
    language_skills = context.user_data.get("language_skills", "N/A")
    last_university_project = context.user_data.get("last_university_project", "N/A")
    project_gpa = context.user_data.get("project_gpa", "N/A")
    hobbies = context.user_data.get("hobbies", "N/A")
    interesting_courses = context.user_data.get("interesting_courses", "N/A")
    user_phone_formatted = f"+98{user_phone[1:]}"

    # Create a link to the user's ID
    user_id_link = f"https://t.me/{convert_farsi_numerals(user_phone_formatted)}"

    user_chat_id = update.effective_message.chat_id
    # Prepare the callback data for the button
    callback_data = f"send {user_chat_id}"
    # Create the inline keyboard markup
    keyboard = [[InlineKeyboardButton(text="Reply to this user", callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)


    # Forward all the information to the admin
    message_text = f"فرم رزومه\nUser details:\nName: {user_name}\nPhone: {user_phone}\nEmail: {user_email}\nTelegram Username: @{telegram_username}\n" \
                   f"Age: {age}\nUniversity: {university}\nMajor: {major}\nGPA: {gpa}\nDesired Major: {desired_major}\nDesired University: {desired_university}\nStudy Duration: {study_duration}\n" \
                   f"Projects: {projects}\nSkills: {skills}\nWork Experience: {work_experience}\nStudy Purpose: {study_purpose}\nBirth Date: {birth_date}\nLanguage Skills: {language_skills}\n" \
                   f"Last University Project: {last_university_project}\nProject GPA: {project_gpa}\nHobbies: {hobbies}\nInteresting Courses: {interesting_courses}\n User Link:{user_id_link}"


    # Send the message without inline keyboard
    context.bot.send_message(chat_id=admin_user_id, text=message_text, reply_markup=reply_markup)
    context.bot.send_photo(chat_id=admin_user_id, photo=open(image_path, "rb"))
    context.bot.send_photo(chat_id=admin_user_id, photo=open(photo_path, "rb"))

    update.message.reply_text("اطلاعات شما با موفقیت ثبت شد. با تشکر!")
    start(update, context)
    return ConversationHandler.END

####################################فرم انگیزه نامه #######################
def start_motivation_form(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لطفاً نام و نام خانوادگی خود را وارد کنید:",
        reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Clear user_data to start with a clean slate
    return MOTIVATION_NAME

def collect_motivation_name(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_name"] = update.message.text
    update.message.reply_text("لطفاً سن خود را وارد کنید:")
    return MOTIVATION_AGE

def collect_motivation_age(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_age"] = update.message.text
    update.message.reply_text("لطفاً شماره موبایل متصل به تلگرام خود را وارد کنید:")
    return MOTIVATION_PHONE

def collect_motivation_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_phone"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه محل تحصیل خود را وارد کنید:")
    return MOTIVATION_UNIVERSITY

def collect_motivation_university(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_university"] = update.message.text
    update.message.reply_text("لطفاً رشته محل تحصیل خود را وارد کنید:")
    return MOTIVATION_MAJOR

def collect_motivation_major(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_major"] = update.message.text
    update.message.reply_text("لطفاً معدل خود را وارد کنید:")
    return MOTIVATION_GPA

def collect_motivation_gpa(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_gpa"] = update.message.text
    update.message.reply_text("لطفاً رشته مورد نظر خود را وارد کنید:")
    return MOTIVATION_DESIRED_MAJOR

def collect_motivation_desired_major(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_desired_major"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه مورد نظر خود را وارد کنید:")
    return MOTIVATION_DESIRED_UNIVERSITY

def collect_motivation_desired_university(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_desired_university"] = update.message.text
    update.message.reply_text("پروژه و تحقیقاتی که طی دوران تحصیل انجام داده‌اید را بنویسید:")
    return MOTIVATION_PROJECTS

def collect_motivation_projects(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_projects"] = update.message.text
    update.message.reply_text("لطفاً مهارت‌ها و برنامه‌هایی که در دانشگاه یا در زمینه کاری کار کرده‌اید، بنویسید (همراه با گواهینامه‌ها و مدارک):")
    return MOTIVATION_SKILLS

def collect_motivation_skills(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_skills"] = update.message.text
    update.message.reply_text("سابقه کار خود را اگر دارید بنویسید:")
    return MOTIVATION_WORK_EXPERIENCE

def collect_motivation_work_experience(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_work_experience"] = update.message.text
    update.message.reply_text("هدف شما از خواندن این رشته چیست؟")
    return MOTIVATION_STUDY_PURPOSE

def collect_motivation_study_purpose(update: Update, context: CallbackContext) -> int:
    context.user_data["motivation_study_purpose"] = update.message.text
    update.message.reply_text("")
    return MOTIVATION_BANK_RECEIPT

def collect_motivation_bank_receipt(update: Update, context: CallbackContext) -> int:
    # Save the photo of the bank receipt for further processing
    image_directory = "images/motivation_bank_receipts/"
    os.makedirs(image_directory, exist_ok=True)
    image_path = image_directory + f"{update.message.from_user.id}_motivation_bank_receipt.jpg"
    update.message.photo[-1].get_file().download(image_path)
    
    # Update user_data with the bank receipt photo path
    context.user_data["motivation_bank_receipt"] = image_path

    # Get user information
    motivation_name = context.user_data.get("motivation_name", "N/A")
    motivation_age = context.user_data.get("motivation_age", "N/A")
    motivation_phone = context.user_data.get("motivation_phone", "N/A")
    motivation_university = context.user_data.get("motivation_university", "N/A")
    motivation_major = context.user_data.get("motivation_major", "N/A")
    motivation_gpa = context.user_data.get("motivation_gpa", "N/A")
    motivation_desired_major = context.user_data.get("motivation_desired_major", "N/A")
    motivation_desired_university = context.user_data.get("motivation_desired_university", "N/A")
    motivation_projects = context.user_data.get("motivation_projects", "N/A")
    motivation_skills = context.user_data.get("motivation_skills", "N/A")
    motivation_work_experience = context.user_data.get("motivation_work_experience", "N/A")
    motivation_study_purpose = context.user_data.get("motivation_study_purpose", "N/A")
    motivation_bank_receipt = context.user_data.get("motivation_bank_receipt", "N/A")
    telegram_username = update.message.from_user.username
    user_phone_formatted = f"+98{motivation_phone[1:]}"
    user_chat_id = update.effective_message.chat_id
    # Prepare the callback data for the button
    callback_data = f"send {user_chat_id}"
    # Create the inline keyboard markup
    keyboard = [[InlineKeyboardButton(text="Reply to this user", callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    

    # Create a link to the user's ID
    user_id_link = f"https://t.me/{convert_farsi_numerals(user_phone_formatted)}"

    # Forward the bank receipt and user information to the admin
    message_text = f"فرم انگیزه نامه\nMotivation form details received from @{telegram_username}:\nUser Link:{user_id_link}\n Name: {motivation_name}\nAge: {motivation_age}\nPhone: {motivation_phone}\nUniversity: {motivation_university}\nMajor: {motivation_major}\nGPA: {motivation_gpa}\nDesired Major: {motivation_desired_major}\nDesired University: {motivation_desired_university}\nProjects: {motivation_projects}\nSkills: {motivation_skills}\nWork Experience: {motivation_work_experience}\nStudy Purpose: {motivation_study_purpose}"

    # Send the message without inline keyboard
    context.bot.send_message(chat_id=admin_user_id, text=message_text, reply_markup=reply_markup)
    context.bot.send_photo(chat_id=admin_user_id, photo=open(image_path, "rb"))

    update.message.reply_text("اطلاعات شما با موفقیت ثبت شد. با تشکر!")
    start(update, context)
    return ConversationHandler.END


###################################### فرم توصیه نامه ##########################

def start_recommendation_form(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لطفاً نام و نام خانوادگی خود را وارد کنید:",
        reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Clear user_data to start with a clean slate
    return RECOMMENDATION_NAME

def collect_recommendation_name(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_name"] = update.message.text
    update.message.reply_text("لطفاً شماره موبایل متصل به تلگرام خود را وارد کنید:")
    return RECOMMENDATION_PHONE

def collect_recommendation_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_phone"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه محل تحصیل خود را وارد کنید:")
    return RECOMMENDATION_UNIVERSITY

def collect_recommendation_university(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_university"] = update.message.text
    update.message.reply_text("لطفاً رشته محل تحصیل خود را وارد کنید:")
    return RECOMMENDATION_MAJOR

def collect_recommendation_major(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_major"] = update.message.text
    update.message.reply_text("لطفاً دانشگاه مورد نظر خود را وارد کنید:")
    return RECOMMENDATION_DESIRED_UNIVERSITY

def collect_recommendation_desired_university(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_desired_university"] = update.message.text
    update.message.reply_text("لطفاً نام استاد مورد نظر و هر درسی که با ایشان پاس کرده‌اید را بنویسید:")
    return RECOMMENDATION_PROFESSOR_NAME

def collect_recommendation_professor_name(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_professor_name"] = update.message.text
    update.message.reply_text("لطفاً نام درس و یا پروژه‌ای که با استاد انجام داده‌اید را بنویسید:")
    return RECOMMENDATION_COURSE_NAME

def collect_recommendation_course_name(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_course_name"] = update.message.text
    update.message.reply_text("لطفاً نمره درس اگر دارید یا توضیح خلاصه‌ای درمورد پروژه را وارد کنید:")
    return RECOMMENDATION_COURSE_GRADE

def collect_recommendation_course_grade(update: Update, context: CallbackContext) -> int:
    context.user_data["recommendation_course_grade"] = update.message.text
    update.message.reply_text("")
    return RECOMMENDATION_BANK_RECEIPT

def collect_recommendation_bank_receipt(update: Update, context: CallbackContext) -> int:
    # Save the photo of the bank receipt for further processing
    image_directory = "images/recommendation_bank_receipts/"
    os.makedirs(image_directory, exist_ok=True)
    image_path = image_directory + f"{update.message.from_user.id}_recommendation_bank_receipt.jpg"
    update.message.photo[-1].get_file().download(image_path)

    # Update user_data with the bank receipt photo path
    context.user_data["recommendation_bank_receipt"] = image_path

    # Get user information
    recommendation_name = context.user_data.get("recommendation_name", "N/A")
    recommendation_phone = context.user_data.get("recommendation_phone", "N/A")
    recommendation_university = context.user_data.get("recommendation_university", "N/A")
    recommendation_major = context.user_data.get("recommendation_major", "N/A")
    recommendation_desired_university = context.user_data.get("recommendation_desired_university", "N/A")
    recommendation_professor_name = context.user_data.get("recommendation_professor_name", "N/A")
    recommendation_course_name = context.user_data.get("recommendation_course_name", "N/A")
    recommendation_course_grade = context.user_data.get("recommendation_course_grade", "N/A")
    telegram_username = update.message.from_user.username
    user_phone_formatted = f"+98{recommendation_phone[1:]}"
    user_chat_id = update.effective_message.chat_id
    # Prepare the callback data for the button
    callback_data = f"send {user_chat_id}"
    # Create the inline keyboard markup
    keyboard = [[InlineKeyboardButton(text="Reply to this user", callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Create a link to the user's ID
    user_id_link = f"https://t.me/{convert_farsi_numerals(user_phone_formatted)}"

    # Forward the bank receipt and user information to the admin
    message_text = (
        f"فرم توصیه نامه\n"
        f"Recommendation form details received from user: @{telegram_username}\n"
        f"Name: {recommendation_name}\n"
        f"Phone: {recommendation_phone}\n"
        f"University: {recommendation_university}\n"
        f"Major: {recommendation_major}\n"
        f"Desired University: {recommendation_desired_university}\n"
        f"Professor Name: {recommendation_professor_name}\n"
        f"Course Name: {recommendation_course_name}\n"
        f"Course Grade: {recommendation_course_grade}\n"
        f"User Link: {user_id_link}"
    )

    # Send the message without inline keyboard
    context.bot.send_message(chat_id=admin_user_id, text=message_text, reply_markup=reply_markup)
    context.bot.send_photo(chat_id=admin_user_id, photo=open(image_path, "rb"))

    update.message.reply_text("اطلاعات شما با موفقیت ثبت شد. با تشکر!")
    start(update, context)
    return ConversationHandler.END

######################################### VIP ##############################################

# Function to start the VIP form
def start_vip_form(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لطفاً نام خانوادگی خود را وارد کنید:",
        reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # Clear user_data to start with a clean slate
    return VIP_FAMILY_NAME

# Function to collect family name for VIP
def collect_vip_family_name(update: Update, context: CallbackContext) -> int:
    context.user_data["vip_family_name"] = update.message.text
    update.message.reply_text("لطفاً شماره موبایل متصل به تلگرام خود را وارد کنید:")
    return VIP_STUDENT_PHONE

# Function to collect student phone for VIP
def collect_vip_student_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["vip_student_phone"] = update.message.text
    update.message.reply_text("لطفاً رشته مقطع تحصیلی خود را وارد کنید:")
    return VIP_STUDENT_MAJOR

# Function to collect student major for VIP
def collect_vip_student_major(update: Update, context: CallbackContext) -> int:
    context.user_data["vip_student_major"] = update.message.text
    update.message.reply_text("لطفاً معدل خود را وارد کنید:")
    return VIP_STUDENT_GPA

# Function to collect student GPA for VIP
def collect_vip_student_gpa(update: Update, context: CallbackContext) -> int:
    context.user_data["vip_student_gpa"] = update.message.text
    update.message.reply_text(".")
    return VIP_STUDENT_BANK_RECEIPT

# Function to collect student bank receipt for VIP
def collect_vip_student_bank_receipt(update: Update, context: CallbackContext) -> int:
    # Save the photo of the bank receipt for further processing
    image_directory = "images/vip_student_bank_receipts/"
    os.makedirs(image_directory, exist_ok=True)
    image_path = image_directory + f"{update.message.from_user.id}_vip_student_bank_receipt.jpg"
    update.message.photo[-1].get_file().download(image_path)

    # Update user_data with the bank receipt photo path
    context.user_data["vip_student_bank_receipt"] = image_path

    # Get user information
    vip_family_name = context.user_data.get("vip_family_name", "N/A")
    vip_student_phone = context.user_data.get("vip_student_phone", "N/A")
    vip_student_major = context.user_data.get("vip_student_major", "N/A")
    vip_student_gpa = context.user_data.get("vip_student_gpa", "N/A"),
    telegram_username = update.message.from_user.username
    user_phone_formatted = f"+98{vip_student_phone[1:]}"
    user_chat_id = update.effective_message.chat_id
    # Prepare the callback data for the button
    callback_data = f"send {user_chat_id}"
    # Create the inline keyboard markup
    keyboard = [[InlineKeyboardButton(text="Reply to this user", callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Create a link to the user's ID
    user_id_link = f"https://t.me/{convert_farsi_numerals(user_phone_formatted)}"

    # Forward the bank receipt and user information to the admin
    message_text = (
        f"VIP:Ask Apply\n"
        f"VIP Student form details received from @{telegram_username}:\n"
        f"Family Name: {vip_family_name}\n"
        f"Student Phone: {vip_student_phone}\n"
        f"Student Major: {vip_student_major}\n"
        f"Student GPA: {vip_student_gpa}\n"
        f"User Link: {user_id_link}"
    )

    # Send the message without inline keyboard
    context.bot.send_message(chat_id=admin_user_id, text=message_text, reply_markup=reply_markup)
    context.bot.send_photo(chat_id=admin_user_id, photo=open(image_path, "rb"))

    update.message.reply_text("اطلاعات شما با موفقیت ثبت شد. با تشکر!")
    start(update, context)
    return ConversationHandler.END




# Conversation handler for starting the chat and providing options
start_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start)
    ],
    states={

    },
    fallbacks=[],
)




# Conversation handler for "Buy Consult" and providing options
buy_consult_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^خرید مشاوره$"), start_buy_consult)],
    states={
        BUY_CONSULT_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_name)],
        BUY_CONSULT_PHONE: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_phone)],
        BUY_CONSULT_EMAIL: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_email)],
        BUY_CONSULT_DEGREE: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_degree)],
        BUY_CONSULT_FIELD: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_field)],
        BUY_CONSULT_AGE: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_age)],
        BUY_CONSULT_DESIRED_FIELD: [MessageHandler(Filters.text & ~Filters.command, collect_buy_consult_desired_field)],
        BUY_CONSULT_BANK_RECEIPT: [MessageHandler(Filters.photo, collect_buy_consult_bank_receipt)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)

# Conversation handler for "فرم رزومه"
resume_form_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex("^فرم رزومه$"), start_resume_form)
    ],
    states={
        RESUME_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_resume_name)],
        RESUME_AGE: [MessageHandler(Filters.text & ~Filters.command, collect_age)],
        RESUME_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_university)],
        RESUME_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_major)],
        RESUME_GPA: [MessageHandler(Filters.text & ~Filters.command, collect_gpa)],
        RESUME_DESIRED_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_desired_major)],
        RESUME_DESIRED_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_desired_university)],
        RESUME_STUDY_DURATION: [MessageHandler(Filters.text & ~Filters.command, collect_study_duration)],
        RESUME_PROJECTS: [MessageHandler(Filters.text & ~Filters.command, collect_projects)],
        RESUME_SKILLS: [MessageHandler(Filters.text & ~Filters.command, collect_skills)],
        RESUME_WORK_EXPERIENCE: [MessageHandler(Filters.text & ~Filters.command, collect_work_experience)],
        RESUME_STUDY_PURPOSE: [MessageHandler(Filters.text & ~Filters.command, collect_study_purpose)],
        RESUME_PHOTO: [MessageHandler(Filters.photo, collect_photo)],
        RESUME_RECOMMENDATIONS: [MessageHandler(Filters.text & ~Filters.command, collect_recommendations)],
        RESUME_EMAIL: [MessageHandler(Filters.text & ~Filters.command, collect_email_resume)],
        RESUME_BIRTH_DATE: [MessageHandler(Filters.text & ~Filters.command, collect_birth_date)],
        RESUME_LANGUAGE_SKILLS: [MessageHandler(Filters.text & ~Filters.command, collect_language_skills)],
        RESUME_LAST_UNIVERSITY_PROJECT: [MessageHandler(Filters.text & ~Filters.command, collect_last_university_project)],
        RESUME_PROJECT_GPA: [MessageHandler(Filters.text & ~Filters.command, collect_project_gpa)],
        RESUME_HOBBIES: [MessageHandler(Filters.text & ~Filters.command, collect_hobbies)],
        RESUME_INTERESTING_COURSES: [MessageHandler(Filters.text & ~Filters.command, collect_interesting_courses)],
        PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, collect_phone_number)],
        BANK_RECEIPT: [MessageHandler(Filters.photo, collect_bank_receipt)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)


# Conversation handler for "فرم انگیزه نامه"
motivation_form_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex("^فرم انگیزه نامه$"), start_motivation_form)
    ],
    states={
        MOTIVATION_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_name)],
        MOTIVATION_AGE: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_age)],
        MOTIVATION_PHONE: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_phone)],
        MOTIVATION_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_university)],
        MOTIVATION_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_major)],
        MOTIVATION_GPA: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_gpa)],
        MOTIVATION_DESIRED_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_desired_major)],
        MOTIVATION_DESIRED_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_desired_university)],
        MOTIVATION_PROJECTS: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_projects)],
        MOTIVATION_SKILLS: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_skills)],
        MOTIVATION_WORK_EXPERIENCE: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_work_experience)],
        MOTIVATION_STUDY_PURPOSE: [MessageHandler(Filters.text & ~Filters.command, collect_motivation_study_purpose)],
        MOTIVATION_BANK_RECEIPT: [MessageHandler(Filters.photo, collect_motivation_bank_receipt)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)


# Conversation handler for "فرم توصیه نامه"
recommendation_form_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex("^فرم توصیه نامه$"), start_recommendation_form),
    ],
    states={
        RECOMMENDATION_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_name)],
        RECOMMENDATION_PHONE: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_phone)],
        RECOMMENDATION_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_university)],
        RECOMMENDATION_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_major)],
        RECOMMENDATION_DESIRED_UNIVERSITY: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_desired_university)],
        RECOMMENDATION_PROFESSOR_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_professor_name)],
        RECOMMENDATION_COURSE_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_course_name)],
        RECOMMENDATION_COURSE_GRADE: [MessageHandler(Filters.text & ~Filters.command, collect_recommendation_course_grade)],
        RECOMMENDATION_BANK_RECEIPT: [MessageHandler(Filters.photo, collect_recommendation_bank_receipt)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Define the VIP form conversation handler
vip_form_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^AskApply$"), start_vip_form)],
    states={
        VIP_FAMILY_NAME: [MessageHandler(Filters.text & ~Filters.command, collect_vip_family_name)],
        VIP_STUDENT_PHONE: [MessageHandler(Filters.text & ~Filters.command, collect_vip_student_phone)],
        VIP_STUDENT_MAJOR: [MessageHandler(Filters.text & ~Filters.command, collect_vip_student_major)],
        VIP_STUDENT_GPA: [MessageHandler(Filters.text & ~Filters.command, collect_vip_student_gpa)],
        VIP_STUDENT_BANK_RECEIPT: [MessageHandler(Filters.photo, collect_vip_student_bank_receipt)],
    },
    fallbacks=[CommandHandler('cancel', cancel)], 
)

def main():
    
    updater = Updater("<BOT-ACCESS-TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(start_conv_handler)
    dp.add_handler(buy_consult_conv_handler)
    dp.add_handler(resume_form_conv_handler)
    dp.add_handler(motivation_form_conv_handler)
    dp.add_handler(recommendation_form_conv_handler)
    dp.add_handler(vip_form_conversation_handler)
    dp.add_handler(CallbackQueryHandler(button_callback, pattern='^send\\s\\d+'))
    dp.add_handler(CommandHandler('send', send_command, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
