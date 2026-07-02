from django.shortcuts import render
from .models import Student

# Maps Arabic-Indic digits (٠-٩) to their Western Arabic (English) equivalents
# so a student ID typed in either numeral system resolves to the same lookup.
ARABIC_INDIC_TO_ENGLISH = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def home(request):
    student = None
    query = ""

    if request.method == "POST":
        query = request.POST.get("student_id", "").strip()

        if query:
            normalized_id = query.translate(ARABIC_INDIC_TO_ENGLISH)
            student = Student.objects.filter(student_id=normalized_id).first()

    context = {
        "student": student,
        "query": query,
    }

    return render(
        request,
        "students/index.html",
        context,
    )
