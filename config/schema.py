# schema.py
import strawberry
from apps.visualization.schema import Query as VisualizationQuery


@strawberry.type
class Query(VisualizationQuery):
    pass


schema = strawberry.Schema(query=Query, )
