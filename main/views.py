from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Shoe, Order, OrderShoe
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm


class HomeView(ListView):
    model = Shoe
    template_name = 'home.html'
    context_object_name = 'shoes'
    paginate_by = 10


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            orders = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            context = {
                'orders': orders
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')
        

class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'product.html'
    context_object_name = 'shoe'

class CheckoutView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'checkout.html')
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('main:checkout')
            messages.warning(self.request, 'Failed checkout')
            return redirect('main:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')


@login_required
def add_to_cart(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    order_item, created = OrderShoe.objects.get_or_create(
        shoe=shoe,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.shoes.filter(shoe__slug=shoe.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('main:order-summary')
        else:
            messages.info(request, "This item was added to your cart.")
            order.shoes.add(order_item)
            return redirect('main:order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.shoes.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('main:order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Shoe, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.shoes.filter(shoe__slug=item.slug).exists():
            order_item = OrderShoe.objects.filter(
                shoe=item,
                user=request.user,
                ordered=False
            )[0]
            order.shoes.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('main:product', slug=slug)
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('main:product', slug=slug)
            
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('main:product', slug=slug)
    

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Shoe, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.shoes.filter(shoe__slug=item.slug).exists():
            order_item = OrderShoe.objects.filter(
                shoe=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.shoes.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect('main:order-summary',)
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('main:product', slug=slug)
            
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('main:product', slug=slug)

# @login_required
def success_payment(request):
    return render(request, 'success_payment.html')

def group_members(request):
    return render(request, 'group-members.html')