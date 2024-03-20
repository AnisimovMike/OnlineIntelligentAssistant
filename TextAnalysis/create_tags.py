import spacy
from WebSite.models import Attractions, AttractionTags
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from shapely.geometry import Polygon, Point
import geopandas as gpd
import pandas as pd


nlp = spacy.load("ru_core_news_md")


def create_tag_by_name(monument_names_list, tag_name):
    object_list = Attractions.objects.filter()
    list_len = len(object_list)
    for i in range(list_len):
        cur_id = object_list[i].id
        name = object_list[i].name
        description = object_list[i].short_description
        name = name.lower()
        description = description.lower()
        doc1 = nlp(name)
        f = False
        for token in doc1:
            for j in monument_names_list:
                cur_str1 = nlp(j.lower())
                cur_str2 = nlp(token.lemma_)
                if cur_str1.similarity(cur_str2) >= 0.8:
                    f = True
                    break
            if f is True:
                break
        if f is True:
            try:
                old_attraction_tag = AttractionTags.objects.get(tag=tag_name, attraction=cur_id)
            except ObjectDoesNotExist:
                attraction_tag = AttractionTags()
                attraction_tag.tag = tag_name
                attraction_tag.attraction = Attractions.objects.get(id=cur_id)
                attraction_tag.save()


def create_tag_location():
    object_list = Attractions.objects.filter()
    mo_gdf = gpd.read_file('mo.geojson')
    n = len(mo_gdf)
    for obj in object_list:
        for i in range(n):
            cur_row = mo_gdf.iloc[i]
            polygon = cur_row['geometry']
            ans = polygon.contains(Point(obj.longitude, obj.latitude))
            if ans:
                cur_area = cur_row['NAME']
                cur_district = cur_row['ABBREV_AO']
                cur_id = obj.id
                try:
                    old_attraction_tag = AttractionTags.objects.get(tag=cur_area, attraction=cur_id)
                except ObjectDoesNotExist:
                    attraction_tag = AttractionTags()
                    attraction_tag.tag = cur_area
                    attraction_tag.attraction = Attractions.objects.get(id=cur_id)
                    attraction_tag.save()
                try:
                    old_attraction_tag = AttractionTags.objects.get(tag=cur_district, attraction=cur_id)
                except ObjectDoesNotExist:
                    attraction_tag = AttractionTags()
                    attraction_tag.tag = cur_district
                    attraction_tag.attraction = Attractions.objects.get(id=cur_id)
                    attraction_tag.save()
