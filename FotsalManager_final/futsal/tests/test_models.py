from django.test import TestCase
from django.contrib.auth.models import User
from futsal import models
from django.core.files.uploadedfile import SimpleUploadedFile

class UserSetup(object):
    
    def setUp(self):
        super().setUp()
        photo = "C:\\Users\\Sharad Bhandari\\Pictures\\3U2gBzq.jpg"
        self.image=SimpleUploadedFile(
                name=photo,
                content=open(photo, 'rb').read(),
                content_type='image/*'
            )
        self.admin = User.objects.create_user(username="admin",password="admin")
        self.user1 = User.objects.create_user(username="user1",password="password")
        self.user2 = User.objects.create_user(username="user2",password="password")
        self.user3 = User.objects.create_user(username="user3",password="password")

    def test_username(self):
        self.assertEquals(self.admin.username,"admin")
        self.assertEquals(self.user1.username,"user1")
        self.assertEquals(self.user2.username,"user2")
        self.assertEquals(self.user3.username,"user3")


class PostModelTest(UserSetup,TestCase):

    def setUp(self):
        super().setUp()
        self.post = models.Post.objects.create(
            owner=self.admin,
            title="Post 1",
            description="Desc1",
            post_image=self.image
        )
        
    def test_create_post(self):
        self.assertEquals(self.post.title,'Post 1')

    def test_cordinator_review(self):
        self.assertNotIn(self.user1,self.post.cordinator_in_review())
        self.assertNotIn(self.user2,self.post.cordinator_in_review())
        self.assertNotIn(self.user3,self.post.cordinator_in_review())

    def test_add_cor_application(self):
        self.post.add_cor_application(self.user1)
        self.assertIn(self.user1,self.post.cordinator_in_review())
        self.assertEquals(models.Coordinator.objects.all().count(),1)
        self.assertEquals(models.Coordinator.objects.filter(coordinator=self.user1,selected=False).exists(),True)

    def test_remove_cor_application(self):
        self.post.remove_cor_application(self.user1)
        self.assertNotIn(self.user1,self.post.cordinator_in_review())
        self.assertEquals(models.Coordinator.objects.all().count(),0)
        self.assertEquals(models.Coordinator.objects.filter(coordinator=self.user1,selected=False).exists(),False)

    def test_add_gm_application(self):
        self.post.add_gm_application(self.user1)
        self.assertIn(self.user1,self.post.gm_in_review())
        self.assertEquals(models.GameManager.objects.all().count(),1)
        self.assertEquals(models.GameManager.objects.filter(game_manager=self.user1,selected=False).exists(),True)

    def test_remove_gm_application(self):
        self.post.remove_gm_application(self.user1)
        self.assertNotIn(self.user1,self.post.gm_in_review())
        self.assertEquals(models.GameManager.objects.all().count(),0)
        self.assertEquals(models.GameManager.objects.filter(game_manager=self.user1,selected=False).exists(),False)

    def test_add_remove_gm_application(self):
        self.test_add_gm_application()
        self.test_remove_gm_application()
        
    def test_add_then_remove_cor_application(self):
        self.test_add_cor_application()
        self.test_remove_cor_application()
        
    def test_assign_cor(self):
        self.post.add_cor_application(self.user1)
        self.assertIn(self.user1,self.post.cordinator_in_review())
        self.post.set_cordinator(self.user1)
        self.assertEquals(self.post.get_cordinator_user(),self.user1)
        self.assertNotIn(self.user1,self.post.cordinator_in_review())

    def test_gm_application(self):
        self.post.add_gm_application(self.user1)
        self.assertIn(self.user1,self.post.gm_in_review())
        self.post.set_gm(self.user1)
        self.assertEquals(self.post.get_gm_user(),self.user1)
        self.assertNotIn(self.user1,self.post.gm_in_review())


