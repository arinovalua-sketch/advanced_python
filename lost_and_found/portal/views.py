from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json

from .models import Item, ItemImage, Claim


# ---------- AUTH ----------
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})


# ---------- FOUND ITEMS ----------
def items_page(request):
    category = request.GET.get('category')

    items = Item.objects.filter(item_type='found')
    if category:
        items = items.filter(category=category)

    return render(request, 'items_list.html', {
        'items': items,
        'page_title': 'Found Items'
    })


# ---------- LOST ITEMS ----------
def lost_items(request):
    category = request.GET.get('category')

    items = Item.objects.filter(item_type='lost')
    if category:
        items = items.filter(category=category)

    return render(request, 'items_list.html', {
        'items': items,
        'page_title': 'Lost Items'
    })


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'items_count': Item.objects.count(),
        'claims_count': Claim.objects.count(),
    })


# ---------- ADD ITEM ----------
@login_required
def add_item(request):
    if request.method == 'POST':
        item = Item.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            item_type=request.POST['item_type'],
            category=request.POST['category'],
            created_by=request.user
        )

        for img in request.FILES.getlist('images'):
            ItemImage.objects.create(
                item=item,
                image=img
            )

        return redirect('/')

    return render(request, 'add_item.html')


# ---------- CLAIM ----------
@login_required
def claim_item(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        Claim.objects.create(
            user=request.user,
            item=item,
            message=request.POST['message']
        )
        return redirect('/')

    return render(request, 'claim.html', {'item': item})

@csrf_exempt
def api_items(request):
    if request.method == 'GET':
        items = list(
            Item.objects.values(
                'id',
                'title',
                'description',
                'location',
                'item_type',
                'category',
                'date_created'
            )
        )
        return JsonResponse(items, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)

        item = Item.objects.create(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            item_type=data['item_type'],
            category=data['category'],
            created_by=request.user if request.user.is_authenticated else 
None
        )

        return JsonResponse({
            'message': 'Item created',
            'item_id': item.id
        })

