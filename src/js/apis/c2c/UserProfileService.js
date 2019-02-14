
function UserProfileService(api) {
  this.api = api;

  this.preferences = {
    get() {
      return api.get('/users/preferences');
    },

    post(preferences) {
      return api.post('/users/preferences', preferences);
    }
  };

  this.mailinglists = {
    get() {
      return api.get('/users/mailinglists');
    },

    post(mailinglists) {
      return api.post('/users/mailinglists', mailinglists);
    }
  };

  this.following = {
    get() {
      return api.get('/users/following');
    },

    add(user_id) {
      return api.post('/users/follow', { user_id });
    },

    remove(user_id) {
      return api.post('/users/unfollow', { user_id });
    },

    isFollowing(user_id) {
      return api.get('/users/following-user/' + user_id);
    }
  };

  this.account = {
    get() {
      return api.get('/users/account');
    },

    post(currentpassword, name, forum_username, email, is_profile_public, newpassword) {
      const payload = {
        currentpassword
      };

      if (name !== null) {
        payload.name = name;
      }

      if (is_profile_public !== null) {
        payload.is_profile_public = is_profile_public;
      }

      if (email !== null) {
        payload.email = email;
      }

      if (forum_username !== null) {
        payload.forum_username = forum_username;
      }

      if (newpassword !== null) {
        payload.newpassword = newpassword;
      }

      return api.post('/users/account', payload);
    }
  };
}

UserProfileService.prototype.login = function(username, password) {
  return this.api.post('/users/login', {
                         username,
                         password,
                         discourse: false
                       },
                       true // safe call : you can do it, even in read-only mode
  );
};

UserProfileService.prototype.update_preferred_language = function(lang) {
  return this.api.post('/users/update_preferred_language', { lang });
};

UserProfileService.prototype.requestPasswordChange = function(email) {
  return this.api.post('/users/request_password_change', { email });
};

UserProfileService.prototype.validateNewPassword = function(nonce, password) {
  return this.api.post('/users/validate_new_password/' + nonce, { password });
};

UserProfileService.prototype.register = function(data) {
  return this.api.post('/users/register', data);
};

UserProfileService.prototype.validateChangeEmail = function(nonce) {
  return this.api.post('/users/validate_change_email/' + nonce);
};

UserProfileService.prototype.validateRegisterEmail = function(nonce) {
  return this.api.post('/users/validate_register_email/' + nonce);
};

export default UserProfileService;
