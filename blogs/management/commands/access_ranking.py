from django.core.management.base import BaseCommand
from blogs.models import Popular
from .analytics_api import print_response


class Command(BaseCommand):
    def handle(self, *args, **options):

        # ブログ閲覧数取得処理
        Popular.objects.all().delete()
        for title, path, view in print_response():
            Popular.objects.create(
                        title=title, path=path, view=view
            )

        # アクセス数取得処理
        # analytics_report = [row for row in print_response_web()]
        # google_access = GoogleAccess
        # google_access.objects.all().delete()

        # for google_value, date_number in zip(analytics_report, reversed(range(len(analytics_report)))):
        #     get_datetime = datetime.date.today() - datetime.timedelta(days=date_number)

        #     google_access.objects.create(
        #             date_data=get_datetime,
        #             access_data=google_value,
        #     )

        self.stdout.write(self.style.SUCCESS('更新完了'))
