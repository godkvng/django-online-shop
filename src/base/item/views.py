from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Item, Category
from .forms import NewItemForm, EditItemForm


def browse(request):
	query = request.GET.get('query', '')
	categories = Category.objects.all()
	category_id = request.GET.get('category',  0)
	items = Item.objects.filter(is_sold=False)

	if category_id:
		items = items.filter(category=category_id)

	if query:
		items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
	context = {
		'items': items,
		'query': query,
		'categories': categories,
		'category_id': int(category_id)
	}
	return render(request, 'item/browse.html', context)


def detail(request, pk):
	items = get_object_or_404(Item, pk=pk)
	related_items = Item.objects.filter(category=items.category, is_sold=False).exclude(pk=pk)[0:3]
	context = {
		'item': items,
		'related_items': related_items,
	}
	return render(request, 'item/detail.html', context)


@login_required
def new_item(request):
	if request.method == 'POST':
		form = NewItemForm(request.POST, request.FILES)
		if form.is_valid():
			item = form.save(commit=False)
			item.created_by = request.user
			item.save()

			return redirect('detail', pk=item.id)
	else:
		form = NewItemForm()
	context = {
		'form': form,
		'title': 'New Item',
	}
	return render(request, 'item/new_item.html', context)


@login_required
def edit_item(request, pk):
	item = get_object_or_404(Item, pk=pk, created_by=request.user)

	if request.method == 'POST':
		form = EditItemForm(request.POST, request.FILES, instance=item)
		if form.is_valid():
			form.save()

			return redirect('detail', pk=item.id)
	else:
		form = EditItemForm(instance=item)
	context = {
		'form': form,
		'title': 'Edit Item',
	}
	return render(request, 'item/new_item.html', context)


@login_required
def delete(request, pk):
	item = get_object_or_404(Item, pk=pk, created_by=request.user)
	item.delete()

	return redirect('dashboard')
