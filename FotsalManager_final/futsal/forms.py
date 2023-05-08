from django import forms 
from . import models

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = ['title','team_image']

class PlayerForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        post = kwargs.pop("post")
        super().__init__(*args, **kwargs)
        if post:
            self.fields["team"].queryset=post.post_teams.all()
            print(self.fields["team"].queryset)
    
    class Meta:
        model = models.Players
        fields = ['team','player','active']


class MatchPlayerForm(forms.ModelForm):    
    class Meta:
        model = models.Players
        fields = ["score"]

class MatchForm(forms.ModelForm):    
    def __init__(self,*args, **kwargs):
        post = kwargs.pop("post",None)
        print(post)
        super().__init__(*args, **kwargs)

        self.fields["team_1"].queryset = post.post_teams.all()
        self.fields["team_2"].queryset = post.post_teams.all()

    class Meta:
        model = models.Match
        fields = ["title","team_1","team_2"]

class MatchFormUpdate(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        self.post = kwargs.pop("post")
        super().__init__(*args, **kwargs)
        if self.post:
            print(self.post)
            self.fields["team_1"].queryset = models.Team.objects.filter(post=self.post) 
            self.fields["team_2"].queryset = models.Team.objects.filter(post=self.post)
            
    class Meta:
        model = models.Match
        fields = ["title","team_1","team_2","completed","draw"]

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = ['title','team_image','match_completed',"score"]
