import uuid
from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import formset_factory
from django.utils.timezone import now, timedelta
from decimal import Decimal
from .models import Passenger, Invoice, Payment, SshCruise, SshPackageInfo, SshTrSrS, Side, Package, Stateroom
from .forms import PassengerForm, StateroomSelectionForm, PackageSelectionForm
from django.http import JsonResponse
from datetime import date, timedelta
import random
import datetime  # Add this import at the top of your views.py file
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Max
import stripe
from django.http import JsonResponse
import json
from collections import Counter

from django.shortcuts import render
import json

def passenger_analysis(request):
    age_groups = {
        "0-10": 5,
        "11-20": 10,
        "21-30": 15,
        "31-40": 7,
        "41+": 3,
    }

    blood_group_count = {
        "A+": 8,
        "B+": 12,
        "O+": 10,
        "AB+": 5,
        "A-": 2,
        "B-": 1,
    }

    gender_count = {
        "Male": 50,
        "Female": 40,
        "Other": 10,
    }

    context = {
        "age_groups": json.dumps(age_groups),
        "blood_group_count": json.dumps(blood_group_count),
        "gender_count": json.dumps(gender_count),
    }
    return render(request, 'passenger_analysis.html', context)


def success(request):
    booking_data = request.session.get('booking_data')

    return render(request, "success.html", {'booking_data': booking_data})

def invoice(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return render(request, 'error.html', {'message': 'Booking data not found.'})
    return render(request, 'invoice.html', {'booking_data': booking_data})

def payment(request):
    # Render payment page with booking data
    
    booking_data = request.session.get('booking_data')
    #print('booking_data',booking_data)
    if not booking_data:
        return redirect('booking')  # Redirect to booking if no booking data is found
    
    return render(request, 'payment.html', {'booking_data': booking_data})

@csrf_exempt
def confirm_payment(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print('k')
    
    
        

        try:
            data = json.loads(request.body)
            print(data)
            payment_method_id = data.get("payment_method_id")
            total_amount = data.get("total_amount")  # Ensure this is passed correctly
            print('data',data)
            stripe.api_key = "sk_test_51QTEgrHlpqUbRcnjAQofgsWjNaIR2vfkfd4QqpjNYQfP2ncJgGJ2cXwqYctsvNBJvkiLXFUonLmBRm9CWfiTeqcZ00qgfTdMxN"  # 
            # Create a payment intent
            # payment_intent = stripe.PaymentIntent.create(
            #     amount=int(float(total_amount) * 100),  # Convert to cents
            #     currency="usd",
            #     payment_method=payment_method_id,
            #     confirm=True,
            # )
            print(f"Payment succeeded: {payment_method_id}")
            #return JsonResponse({"success": True})
        except stripe.error.CardError as e:
            print(f"Payment Failure: {payment_method_id}")
        # Retrieve booking data from session
        booking_data = request.session.get('booking_data')
        #print(booking_data)
        if booking_data:
            print('hi')
            # Generate unique numeric payment_id
            #payment_id = int(datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999)))

            invoice_inst = Invoice.objects.create(
                invoice_id = booking_data['invoice_id'],
                due_date = booking_data['due_date'],
                total_amount = booking_data['total_amount'],
                room_cost = booking_data['cost'],
                package_cost = booking_data['total_package_cost'],
                Date = booking_data['date'],

            )
            payments = Payment.objects.all()
            payments_ids = []
            for payment in payments:
                try:
                    # Convert payment_id to an integer
                    payments_ids.append(int(payment.payment_id))
                    
                except ValueError:
                    print(f"Failed to convert Payment ID: {payment.payment_id} to an integer")

            last_payment_id = max(payments_ids)
            #last_payment_id = last_payment['payment_id__max']

            # Increment the payment_id
            if last_payment_id is None:
                # Start with an initial value if no payment exists
                new_payment_id = 1
            else:
                new_payment_id = int(last_payment_id) + 1
            
            invoice = Invoice.objects.filter(
                due_date=booking_data['due_date'],
                total_amount=booking_data['total_amount'],
            ).first() 

            Payment.objects.create(
                payment_id=new_payment_id,
                payment_date=booking_data['date'],
                payment_amount=booking_data['total_amount'],
                payment_method='Credit Card',
                ssh_invoice_invoice_id=invoice,
            )
            print('booking_data', booking_data)
            passengers = booking_data['passengers']
            for passenger_data in passengers:
                try:
                    # Check if passenger exists
                    passenger = Passenger.objects.filter(
                        first_name = passenger_data['first_name'],
                        last_name = passenger_data['last_name'],
                        date_of_birth = passenger_data['date_of_birth'],   
                    ).first()

                    if passenger:
                        # Update existing passenger
                        for key, value in passenger_data.items():
                            setattr(passenger, key, value)
                        passenger.save()
                    else:
                        # Insert new passenger
                        passenger = Passenger.objects.create(**passenger_data)

                    
                except Exception as e:
                    print(f"Error processing passenger: {passenger_data}. Error: {e}")
                    continue

            print("Passengers processed successfully.")

            # Redirect to the success page
            print("Redirecting to the success page...")
            return render(request, 'success.html', {"booking_data": booking_data})

            #return render(request, 'success.html', {"booking_data": booking_data})

            #return render(request, 'success.html', {"booking_data": booking_data})

        # If booking data is missing, redirect to the booking page
        #return redirect('booking')

    # Handle non-POST requests (optional)
    return redirect('booking')


@csrf_exempt  # Allow POST requests from your form
def process_booking(request):
    if request.method == 'POST':
        # Get the number of passengers
        num_passengers = int(request.POST.get('num_passengers', 1))

        # Collect passenger details
        passengers = []
        for i in range(1, num_passengers + 1):
            passenger_data = {
                'first_name': request.POST.get(f'first_name_{i}', '').strip(),
                'last_name': request.POST.get(f'last_name_{i}', '').strip(),
                'date_of_birth': request.POST.get(f'date_of_birth_{i}', '').strip(),
                'blood_group': request.POST.get(f'blood_group_{i}', '').strip(),
                'street_address': request.POST.get(f'street_address_{i}', '').strip(),
                'city': request.POST.get(f'city_{i}', '').strip(),
                'state': request.POST.get(f'state_{i}', '').strip(),
                'country': request.POST.get(f'country_{i}', '').strip(),
                'zip_code': request.POST.get(f'zip_code_{i}', '').strip(),
                'phone_number': request.POST.get(f'phone_number_{i}', '').strip(),
            }
            passengers.append(passenger_data)

        # Get stateroom and side selections
        stateroom_id = request.POST.get('stateroom', None)
        stateroom = Stateroom.objects.get(pk=stateroom_id) if stateroom_id else None

        side_id = request.POST.get('side', None)
        side = Side.objects.get(pk=side_id) if side_id else None


        cost = None
        if stateroom and side:
            try:
                record = SshTrSrS.objects.get(stateroom_id=stateroom.stateroom_id, side_id=side.side_id, trip_id='T001')
                cost = float(record.price_per_night)
            except SshTrSrS.DoesNotExist:
                cost = 0.0

        stateroom_data = {
            'id': stateroom.stateroom_id,
            'type': stateroom.type,
            'number_of_beds': stateroom.number_of_bed,
        } if stateroom else None

        side_data = {
            'id': side.side_id,
            'name': side.side_name,
        } if side else None

        # Get selected packages
        package_ids = request.POST.getlist('packages')
        packages = Package.objects.filter(pk__in=package_ids)
        packages_data = [
            {'package_name': package.package_name, 'cost': float(package.cost)}
            for package in packages
        ]

        # Calculate total package cost
        total_package_cost = sum(package['cost'] for package in packages_data)

        # Fetch the last invoice_id
        last_invoice = Invoice.objects.aggregate(Max('invoice_id'))
        last_invoice_id = last_invoice['invoice_id__max']

        # Increment the invoice_id
        if last_invoice_id is None:
            # Start with an initial value if no invoice exists
            new_invoice_id = 1
        else:
            new_invoice_id = last_invoice_id + 1
        today = date.today()
        due_date = today + timedelta(days=7)

        total_amount = (cost or 0.0) + total_package_cost

        # Prepare booking data
        booking_data = {
            'invoice_id': new_invoice_id,
            'date': today.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'num_passengers': num_passengers,
            'passengers': passengers,
            'stateroom': stateroom_data,
            'side': side_data,
            'packages': packages_data,
            'total_package_cost': total_package_cost,
            'cost': cost,
            'total_amount': total_amount,
        }

        # Save booking_data in session
        request.session['booking_data'] = booking_data

        # Render the invoice page
        return render(request, 'booking_summary.html', {'booking_data': booking_data})

    return render(request, 'booking.html')


def booking(request):
    """Main booking page view."""
    if request.method == 'POST':
        num_passengers = int(request.POST.get('num_passengers', 1))
        
        # Logic for filtering staterooms based on number of passengers
        if num_passengers > 4:
            staterooms = Stateroom.objects.filter(number_of_bed=6)
        elif num_passengers > 3:
            staterooms = Stateroom.objects.filter(number_of_bed__in=[4, 6])
        elif num_passengers > 1:
            staterooms = Stateroom.objects.filter(number_of_bed__in=[2, 4, 6])
        else:
            staterooms = Stateroom.objects.filter(number_of_bed__in=[1, 2, 4, 6])

        # Dynamically set the queryset for the stateroom selection form
        stateroom_form = StateroomSelectionForm()
        stateroom_form.fields['stateroom'].queryset = staterooms
        
        package_form = PackageSelectionForm()

        return render(request, 'booking.html', {
            'num_passengers': num_passengers,
            'stateroom_form': stateroom_form,
            'package_form': package_form,
        })
    else:
        # Initial view setup
        stateroom_form = StateroomSelectionForm()
        package_form = PackageSelectionForm()

        return render(request, 'booking.html', {
            'num_passengers': 1,
            'stateroom_form': stateroom_form,
            'package_form': package_form,
        })
    
def calculate_cost(request):
    stateroom_id = request.GET.get('stateroom_id')
    side_id = request.GET.get('side_id')
    trip_id = request.GET.get('trip_id')

    try:
        cost_entry = SshTrSrS.objects.get(
            stateroom_id=stateroom_id,
            side_id=side_id,
            trip_id=trip_id
        )
        return JsonResponse({'cost': float(cost_entry.price_per_night)})
    except SshTrSrS.DoesNotExist:
        return JsonResponse({'error': 'Cost not found for the given parameters.'}, status=404)
    

# def complete_booking(request):
#     PassengerFormSet = formset_factory(PassengerForm, extra=0)
#     StateroomForm = StateroomSelectionForm()
#     PackageForm = PackageSelectionForm()

#     if request.method == 'POST':
#         num_passengers = int(request.POST.get('num_passengers', 0))
#         PassengerFormSet = formset_factory(PassengerForm, extra=num_passengers)
#         passenger_formset = PassengerFormSet(request.POST, prefix='passenger')
#         stateroom_form = StateroomSelectionForm(request.POST)
#         package_form = PackageSelectionForm(request.POST)

#         if passenger_formset.is_valid() and stateroom_form.is_valid() and package_form.is_valid():
#             with transaction.atomic():
#                 group_id = uuid.uuid4().hex[:8].upper()
#                 passenger_data_list = passenger_formset.cleaned_data
#                 stateroom = 1
#                 side = 1
#                 packages = package_form.cleaned_data['packages']

#                 stateroom_cost = SshTrSrS.objects.get(
#                     stateroom=stateroom, side=side, trip_id="TRIP01"
#                 ).price_per_night * len(passenger_data_list)

#                 package_cost = sum(package.cost for package in packages)
#                 total_cost = stateroom_cost + package_cost

#                 invoice = Invoice.objects.create(
#                     due_date=now().date() + timedelta(days=7),
#                     total_amount=Decimal(total_cost),
#                     room_cost=Decimal(stateroom_cost),
#                     package_cost=Decimal(package_cost),
#                 )

#                 for passenger_data in passenger_data_list:
#                     passenger, created = Passenger.objects.update_or_create(
#                         first_name=passenger_data['first_name'],
#                         last_name=passenger_data['last_name'],
#                         date_of_birth=passenger_data['date_of_birth'],
#                         defaults=passenger_data
#                     )
#                     SshCruise.objects.create(
#                         ssh_trip_trip_id='TRIP01',
#                         ssh_passenger_passenger_id=passenger.passenger_id,
#                         group_id=group_id,
#                         ssh_stateroom_stateroom_id=stateroom.stateroom_id,
#                         ssh_sides_side_id=side.side_id
#                     )
#                     for package in packages:
#                         SshPackageInfo.objects.create(
#                             package_id=package.package_id,
#                             trip_id='TRIP01',
#                             passenger_id=passenger.passenger_id,
#                             group_id=group_id
#                         )

#                 return render(request, 'booking_summary.html', {
#                     'invoice': invoice,
#                     'stateroom_cost': stateroom_cost,
#                     'package_cost': package_cost,
#                     'total_cost': total_cost,
#                     'passengers': passenger_data_list,
#                     'stateroom': stateroom,
#                     'side': side,
#                     'packages': packages,
#                 })
#     else:
#         passenger_formset = PassengerFormSet(prefix='passenger')

#     return render(request, 'complete_booking.html', {
#         'passenger_formset': passenger_formset,
#         'stateroom_form': StateroomForm,
#         'package_form': PackageForm,
#     })

# from django.shortcuts import render
# from django.http import JsonResponse

# def trial(request):
#     num_passenger = 3
#     print('hi')  # Debug statement to ensure the function is called

#     try:
#         # Fetch all staterooms with number_of_bed = 6
#         if num_passenger > 4:
#             staterooms = Stateroom.objects.filter(number_of_bed=6)
#         elif num_passenger > 3:
#             staterooms = Stateroom.objects.filter(number_of_bed__in=[4, 6])
#         elif num_passenger > 1:
#             staterooms = Stateroom.objects.filter(number_of_bed__in=[2, 4, 6])
#         else:
#             staterooms = Stateroom.objects.filter(number_of_bed__in=[1, 2, 4, 6])
        
#         # Serialize the stateroom data to a list of dictionaries
#         stateroom_data = [
#             {
#                 'id': stateroom.stateroom_id,
#                 'type': stateroom.type,
#                 'size': stateroom.size,
#                 'number_of_bed': stateroom.number_of_bed,
#             }
#             for stateroom in staterooms
#         ]

#         # Fetch the first side
#         side = Side.objects.first()

#         # Serialize the side data to a dictionary (if a side exists)
#         side_data = {
#             'id': side.side_id,
#             'side_name': side.side_name,
#         } if side else {}

#         print("Stateroom Data:", stateroom_data)
#         print("Side Data:", side_data)

#         # Pass data to the template for rendering
#         return render(request, 'trial.html', {
#             'stateroom_data': stateroom_data,
#             'side_data': side_data,
#         })

#     except Exception as e:
#         print(f"Error: {e}")
#         return JsonResponse({'error': 'An error occurred'}, status=500)
