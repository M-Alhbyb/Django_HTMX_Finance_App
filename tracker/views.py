from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from tracker.charting import plot_category_pie_chart, plot_income_expense_bar
from tracker.filters import TransactionFilter
from tracker.forms import TransactionForm
from tracker.models import Transaction


from .resources import TransactionResource

from tablib import Dataset
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "tracker/index.html")


@login_required
def transactions_list(request):
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )
    paginator = Paginator(transactions_filter.qs, settings.PAGE_SIZE)
    transactions_page = paginator.page(1)
    total_income = transactions_filter.qs.get_total_income()
    total_expenses = transactions_filter.qs.get_total_expenses()

    context = {
        "transactions": transactions_page,
        "filter": transactions_filter,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": total_income - total_expenses,
    }

    if request.htmx:
        return render(request, "tracker/partials/transactions_container.html", context)

    return render(request, "tracker/transactions_list.html", context)


@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {"message": "Transaction Added Successfully!"}
            return render(request, "tracker/partials/transaction_success.html", context)
        else:
            context = {"form": form}
            return render(request, "tracker/partials/create_transaction.html", context)

    context = {"form": TransactionForm}
    return render(request, "tracker/partials/create_transaction.html", context)


def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            # context = {"message": "Transaction Updated Successfully!"}
            # return render(
            #     request, "tracker/partials/transaction_success_update.html", context
            # )

            messages.success(request, "Transaction Updated successfully!")
            return redirect('transactions-list')
        
        # else:
        #     context = {"form": form, "transaction": transaction}
        # return render(request, "tracker/partials/update_transaction.html", context)

    context = {
        "form": TransactionForm(instance=transaction),
        "transaction": transaction,
    }
    return render(request, "tracker/partials/update_transaction.html", context)


@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    messages.success(request, "Transaction deleted successfully!")
    # return redirect("tracker/transactions_list.html")
    return redirect('transactions-list')
    # context = {
    #     "message": f"Transaction of ${transaction.amount} on {transaction.date} Deleted Successfully"
    # }
    # return render(request, "tracker/partials/transaction_success_delete.html", context)


@login_required
def get_transactions(request):
    import time

    time.sleep(1)
    page = request.GET.get("page", 1)
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )
    paginator = Paginator(transactions_filter.qs, settings.PAGE_SIZE)
    context = {"transactions": paginator.page(page)}
    return render(
        request,
        "tracker/partials/transactions_container.html#transactions-partial",
        context,
    )


def transactions_charts(request):
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )

    income_expense_bar = plot_income_expense_bar(transactions_filter.qs)

    category_income_pie = plot_category_pie_chart(
        transactions_filter.qs.filter(type="income"), type="Income"
    )
    category_expense_pie = plot_category_pie_chart(
        transactions_filter.qs.filter(type="expense"), type="Expense"
    )

    context = {
        "filter": transactions_filter,
        "income_expense_barchart": income_expense_bar.to_html(),
        "category_income_pie": category_income_pie.to_html(),
        "category_expense_pie": category_expense_pie.to_html(),
    }

    if request.htmx:
        return render(request, "tracker/partials/charts_container.html", context)

    return render(request, "tracker/charts.html", context)

@login_required
def export(request):
    if request.htmx:
        return HttpResponse(headers = {'HX-Redirect':request.get_full_path()})

    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related(
            "category"
        ),
    )
    data = TransactionResource().export(transactions_filter.qs)

    response = HttpResponse(data.csv)
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    return response

@login_required
def import_transactions(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        resource = TransactionResource()
        dataset = Dataset()
        dataset.load(file.read().decode(), format="csv")
        result = resource.import_data(dataset, user=request.user, dry_run=True)

        if not result.has_errors():
            resource.import_data(dataset, user=request.user, dry_run=False)
            context ={
                'message':f'{len(dataset)} Transactions Were Imported Successfully'
            }
        else:
            context ={
                'message':'An Error Occured, Try Again!'
            }

        return render(request, "tracker/partials/transaction_success_import.html", context)
    
    return render(request, "tracker/partials/import_transactions.html")