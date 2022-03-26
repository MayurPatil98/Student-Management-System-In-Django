from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Staff, Staff_Notification, Staff_leave, Staff_Feedback, Subject, Session_Year, Student, Attendance, Attendance_Report
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):

    return render(request, 'Staff/home.html')

@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id =i.id


        notification = Staff_Notification.objects.filter(staff_id=staff_id)

        context = {
            'notification': notification
        }
        return render(request, 'Staff/notification.html', context)

@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notifications')

@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff =Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id


        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)

        context = {
            'staff_leave_history': staff_leave_history,
        }
    return render(request, 'Staff/apply_leave.html', context)

@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin=request.user.id)

        leave = Staff_leave(
            staff_id = staff,
            data = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request, 'Leave Send Successfully')
        return redirect('staff_apply_leave')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin= request.user.id)

    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)

    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'Staff/feedback.html', context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin= request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = " ",
        )
        feedback.save()
        return redirect('staff_feedback')


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject = Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students,
    }
    return render(request, 'Staff/take_attendance.html', context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_data=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)
            p_students = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                student_id= p_students,
                attendance_id= attendance,
            )
            attendance_report.save()

        return redirect('staff_take_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin=request.user.id)

    subject = Subject.objects.filter(staff_id=staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_data=attendance_date)

            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'Staff/view_attendance.html', context)
