from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Group, FriendRequest, Bill, Item, Share
from .forms import GroupForm, ItemForm, BillForm
# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
@transaction.atomic
def list_persons(request):
    users = User.objects.all().select_related('person')
    others = users.exclude(id=request.user.id)
    people = request.user.person.friends.all()
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
    you = request.user

    for i in people:
        others = others.exclude(id=i.id).select_related('person')
    for j in sent_friend_requests:
        if j.from_user == request.user:
            others = others.exclude(id=j.to_user.id).select_related('person')
    for l in rec_friend_requests:
        if l.to_user == request.user:
            others = others.exclude(id=l.from_user.id).select_related('person')

    mygroups = Group.objects.filter(current_user=request.user.person)

    return render(request, 'persons.html', {'users': users, 'people': people, 'mygroups': mygroups, 'others': others,
                                            'sent_friend_requests': sent_friend_requests,
                                            'rec_friend_requests': rec_friend_requests, 'you': you})


# def update_persons(request, user_id):
#     person = Person.objects.get(id=user_id)
#     form = PersonForm(request.POST or None, instance=person)
#
#     if form.is_valid():
#         form.save()
#         return redirect('list_persons')

#   return render(request, 'persons-form.html', {'form': form, 'person': person})


def list_users(request, mygroup):
    people = request.user.person.friends.all().exclude(myGroup__name=mygroup)
    clickedgroup = User.objects.all().filter(myGroup__name=mygroup)
    group_bills = Bill.objects.filter(group=mygroup)
    you = request.user
    return render(request, 'users.html',
                  {'clickedgroup': clickedgroup, 'people': people, 'mygroup': mygroup, 'group_bills': group_bills,
                   'you': you})


def create_group(request):
    form = GroupForm(request.POST or None)

    if form.is_valid():
        myGroup = form.save(commit=False)
        myGroup.current_user = request.user.person
        myGroup.save()
        return redirect('list_persons')

    return render(request, 'persons-form.html', {'form': form})


def add_to_group(request, operation, user_id, mygroup):
    new_joiner = User.objects.get(id=user_id)
    current_group = Group.objects.get(name=mygroup)
    if operation == 'add':
        current_group.myGroup.add(new_joiner)
        joiner_share = Share.objects.create(group=mygroup, amount=0)
        new_joiner.person.shares.add(joiner_share)
    elif operation == 'remove':
        x = new_joiner.person.shares.get(group=mygroup)
        if x.amount == 0.00:
            x.delete()
            current_group.myGroup.remove(new_joiner)


    return redirect('list_users', mygroup)


def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return redirect('list_persons')


def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return redirect('list_persons')


def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.person.friends.add(user2)
    user2.person.friends.add(user1)
    frequest.delete()
    return redirect('list_persons')


def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return redirect('list_persons')


def create_bill(request, mygroup):
    bill_form = BillForm(request.POST or None)

    people_in_group = User.objects.all().filter(myGroup__name=mygroup)

    if bill_form.is_valid():
        mybill = bill_form.save(commit=False)
        mybill.group = mygroup
        mybill.bill_maker = request.user
        bill_id = mybill.id
        mybill.save()

        return redirect('edit_bill', bill_id)
    return render(request, 'create _bill.html', {'bill_form': bill_form})


def edit_bill(request, mybill):
    mybill_object = Bill.objects.get(id=mybill)
    m = mybill_object.no_items
    n = range(m)
    ids = []
    unsaved = []
    action_group = Group.objects.filter(name=mybill_object.group).first()
    members = User.objects.filter(myGroup__name=action_group)
    s = members.count()
    sum = 0
    f_list = [ItemForm(request.POST or None, prefix=str(x)) for x in n]
    if all(form.is_valid() for form in f_list):

        for form in f_list:
            unsaved.append(form.save(commit=False))
        for l in unsaved:
            l.item_bill = mybill_object
            ids.append(l.id)
            l.save()
            this_item = Item.objects.get(id=ids[-1])
            mybill_object.items.add(this_item)
            sum += this_item.price
        for k in members:
            x = k.person.shares.filter(group=action_group)
            y = k.person.shares.get(group=action_group)
            x.update(amount=y.amount - sum/s)

            one = Person.objects.get(user=k)
            mem = Person.objects.filter(user=k)
            mem.update(money=one.money - sum/s)


        return redirect('list_users', mybill_object.group)
    else:

        f_list = [ItemForm(prefix=str(x)) for x in n]

    return render(request, 'editbill.html', {'f_list': f_list, 'mybill_object':  mybill_object, 'n': n})

#
#
# def update_persons(request, id):
#     person = Person.objects.get(id=id)
#     form = PersonForm(request.POST or None, instance=person)
#
#     if form.is_valid():
#         form.save()
#         return redirect('list_persons')
#
#     return render(request, 'persons-form.html', {'form': form, 'person': person})
#
#
# def update_users(request, id):
#     user = User.objects.get(id=id)
#     form = UserCreationForm(request.POST or None, instance=user)
#
#     if form.is_valid():
#         form.save()
#         return redirect('list_users')
#
#     return render(request, 'persons-form.html', {'form': form, 'user': user})
#
#
# def delete_persons(request, id):
#     person = Person.objects.get(id=id)
#
#     if request.method == 'POST':
#         person.delete()
#         return redirect('list_persons')
#
#     return render(request, 'create _bill.html', {'person': person})
