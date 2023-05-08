from django.db import models
from core.abstract import CreateUpdatedModelMixin
from django.contrib.auth.models import User

class Post(CreateUpdatedModelMixin, models.Model):
    owner = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    description = models.TextField()
    post_image = models.ImageField(upload_to="post/")
    coordinators = models.ManyToManyField("auth.User",related_name="cor_application",through="Coordinator")
    game_managers = models.ManyToManyField("auth.User",related_name="gm_application",through="GameManager")
    completion_status = models.BooleanField(default=False)
    winner = models.ForeignKey("Team",related_name="final_winner",on_delete=models.SET_NULL,null=True,blank=True)

    def cordinator_in_review(self):
        """Return list of User from application list that is not accepted"""
        return User.objects.filter(
            models.Q(coordinator__selected=False) &
            models.Q(coordinator__post=self)
        )

    
    def gm_in_review(self):
        """Return list of User from application list that is not accepted"""
        return User.objects.filter(
            models.Q(gamemanager__selected=False) &
            models.Q(gamemanager__post=self)
        )

    def get_gm_object(self):
        if not hasattr(self,"game_object"):
            self.game_object = GameManager.objects.filter(post=self)
        return self.game_object
    
    def get_cordinator_object(self):
        if not hasattr(self,"cor_object"):
            self.cor_object = Coordinator.objects.filter(post=self)
        return self.cor_object
    
    def get_cordinator_obj(self):
        """Get the selected cordinator instance from this object"""
        if not hasattr(self,"selected_cordinator"):
            qs = self.get_cordinator_object()
            self.selected_cordinator = qs.filter(selected=True).distinct().first()
        return self.selected_cordinator
    
    def get_gm_obj(self):
        """Get the selected game_manager instance of this object"""
        if not hasattr(self,"selected_gm"):
            qs = self.get_gm_object()
            self.selected_gm = qs.filter(selected=True).distinct().first() 
        return self.selected_gm
    
    def get_cordinator_user(self):
        """Get user instance of cordinator"""
        cor_object = self.get_cordinator_obj()
        if cor_object:
            return cor_object.coordinator
        return None
    
    def get_gm_user(self):
        """Get user instance of game_manager"""
        gm_object = self.get_gm_obj()
        if gm_object:
            return gm_object.game_manager
        return None
    
    def set_cordinator(self,user):
        Coordinator.objects.filter(post=self,selected=True).update(selected=False)
        if User.objects.filter(id=user.id).exists():
            Coordinator.objects.filter(post=self,coordinator=user).update(selected=True)
            return True 
        return False
    
    def unset_cordinator(self):
        Coordinator.objects.filter(post=self,selected=True).update(selected=False)
        return True
    
    def unset_gm(self):
        GameManager.objects.filter(post=self,selected=True).update(selected=False)
        return True
    
    def set_gm(self,user):
        GameManager.objects.filter(post=self,selected=True).update(selected=False)
        if User.objects.filter(id=user.id).exists():
            GameManager.objects.filter(post=self,game_manager=user).update(selected=True)
            return True 
        return False

    

    def add_cor_application(self,user):
        if user not in self.cordinator_in_review():
            self.coordinators.add(user,through_defaults={"selected":False})
            return True
        return False
    
    def add_gm_application(self,user):
        if user not in self.gm_in_review():
            self.game_managers.add(user,through_defaults={"selected":False})
            return True
        return False
    
    def remove_cor_application(self,user):
        if user in self.cordinator_in_review():
            self.coordinators.remove(user)
            return True
        return False
    
    def remove_gm_application(self,user):
        if user in self.gm_in_review():
            self.game_managers.remove(user)
            return True
        return False
    

    def is_cordinator(self,user):
        """Check if request user is cordinator of this object"""
        cor_object = self.get_cordinator_user()
        if cor_object:
            if user == cor_object:
                return True
        return False
    
    def is_gm(self,user):
        """Check if request user is game_manager of this object"""
        gm_object = self.get_gm_user()
        if gm_object:
            if user == gm_object:
                return True
        return False
    
    def get_winner(self):
        """Get winner of this object"""
        cor_object = self.get_cordinator_obj()
        if cor_object:
            team_list = Team.objects.filter(coordinator=cor_object)
            max_score = team_list.aggregate(max_score=models.Max("score"))["max_score"]
            return team_list.filter(score=max_score).first()
        return None 
    
    def get_all_teams(self):
        cor_obj = self.get_cordinator_obj()
        gm_obj = self.get_gm_obj()
        return Team.objects.filter(coordinator=cor_obj,game_manager=gm_obj)

    def __str__(self):return self.title

class Team(CreateUpdatedModelMixin,models.Model):
    post = models.ForeignKey("Post",on_delete=models.CASCADE,related_name="post_teams")
    team_image = models.ImageField(upload_to="team_image/")
    title = models.CharField(max_length=240)
    players = models.ManyToManyField("auth.User", through="Players",related_name="player_teams")
    score = models.PositiveBigIntegerField(default=0)
    match_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def players_count(self):
        return self.players.all().count()
    
    def all_players(self):
        return Players.objects.filter(post=self.post,team=self)

class Coordinator(CreateUpdatedModelMixin,models.Model):
    post = models.ForeignKey("Post",on_delete=models.CASCADE)
    coordinator = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)

class Match(CreateUpdatedModelMixin,models.Model):
    post = models.ForeignKey("Post",related_name="post_matches",on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    team_1 = models.ForeignKey("Team",related_name="team1_match",on_delete=models.CASCADE)
    team_2 = models.ForeignKey("Team",related_name="team2_match",on_delete=models.CASCADE)
    draw = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    watchers = models.PositiveBigIntegerField(default=0)
    winner = models.ForeignKey("Team",related_name="winner_matches",on_delete=models.SET_NULL,null=True,blank=True)

    def all_players(self):
        return Players.objects.filter(post=self.post,match=self)
    
class Players(CreateUpdatedModelMixin,models.Model):
    post = models.ForeignKey("Post",related_name="post_players",on_delete=models.CASCADE)
    team = models.ForeignKey("Team",related_name="team_player",on_delete=models.CASCADE)
    match = models.ForeignKey("Match",on_delete=models.SET_NULL,null=True,blank=True)
    player = models.ForeignKey("auth.User",related_name="player_scores",on_delete=models.CASCADE)
    score = models.PositiveBigIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):return self.player.get_full_name()
    
class GameManager(CreateUpdatedModelMixin,models.Model):
    post = models.ForeignKey("Post",on_delete=models.CASCADE)
    game_manager = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
