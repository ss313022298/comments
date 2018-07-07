from django.db.models import Q, forms

from utils.datetime_utils import timestamp_to_datetime, datetime_to_timestamp


class GetListForm(forms.Form):
    page_limit = forms.IntegerField(min_value=1, max_value=50, required=False)
    section = forms.CharField(max_length=64, required=False)
    status = forms.IntegerField(min_value=1, max_value=3, required=False)


class GetListHelper:
    @classmethod
    def get_list(cls, condition, model, order_filed, extend_q):
        '''
        返回结果：
        next 是否有下一页
        stop_timestamp 下页最大时间戳
        min_timestamp 下页最小时间戳
        records 结果集
        '''
        q = Q()
        if extend_q:
            q &= extend_q

        if condition.get('company_id'):
            q &= Q(company_id=condition.get('company_id'))

        page_limit = condition.get('page_limit')
        page_limit = page_limit if page_limit else 50

        if condition.get('user_id'):
            q &= Q(user_id=condition.get('user_id'))

        min_timestamp = condition.get('min_timestamp')
        if min_timestamp:
            q &= Q(created_time__gte=timestamp_to_datetime(min_timestamp))
        max_timestamp = condition.get('max_timestamp')
        if max_timestamp:
            q &= Q(created_time__lt=timestamp_to_datetime(max_timestamp))

        status = condition.get('status')

        if status:
            q &= Q(status=status)

        query_set = model.objects.filter(
            q).order_by('-' + order_filed)[:page_limit + 1]
        stop_timestamp = timestamp_to_datetime(max_timestamp)

        records = []
        for record in query_set[:page_limit]:
            records.append(record.brief_info())
            stop_timestamp = record.brief_info()[order_filed]

        stop_timestamp = datetime_to_timestamp(stop_timestamp)
        return len(query_set) > page_limit, stop_timestamp, \
               min_timestamp, records
