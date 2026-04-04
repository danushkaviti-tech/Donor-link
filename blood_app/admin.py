from django.contrib import admin
from .models import Donor, Hospital, DonationRequest

# 1. Customizing the Donor Admin
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    # This controls what columns you see in the list view
    list_display = ('get_name', 'blood_group', 'location', 'phone')
    # This adds a search bar for names and locations
    search_fields = ('user__username', 'location', 'blood_group')
    # This adds a filter sidebar on the right
    list_filter = ('blood_group', 'location')

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Donor Name'

# 2. Customizing the Hospital Admin
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'address')
    list_editable = ('is_verified',) # You can verify hospitals directly from the list!
    search_fields = ('user__username', 'address')

# 3. Customizing the Requests Admin
@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'donor', 'status')
    list_filter = ('status',)