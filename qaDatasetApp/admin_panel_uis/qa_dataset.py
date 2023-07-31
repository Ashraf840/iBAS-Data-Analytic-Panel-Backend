from django.contrib import admin


class QADatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'bangla_ques', 'english_ques', 'transliterated_ques', 'bangla_ans',
                    'english_ans', 'created_by', 'created_at', 'update_at']
    list_display_links = list_display[:1]
    search_fields = list_display
    list_per_page = 15
    ordering = ['-id']
