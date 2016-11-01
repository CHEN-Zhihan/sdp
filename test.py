from general.models import Participant,Instructor,Category,Course


categories = ["Information Technology","Mergers and Acquisitions", "Markets","Risk Management","Securities","Financial Modelling","Operations"]

for c in categories:
    if not Category.objects.filter(name=c).exists():
        Category.create(c)