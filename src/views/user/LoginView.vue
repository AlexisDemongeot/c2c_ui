<template>
  <div class="login-view is-flex">
    <html-header :title="$gettext('Login')" />
    <base-form v-show="mode == 'signin'" :promise="promise" @submit="signin">
      <form-field
        ref="signinMainInput"
        name="username"
        type="text"
        required
        autocapitalize="off"
        autocorrect="off"
        :label="$gettext('Username')"
        v-model="username"
        icon="user"
      />

      <form-field
        :name="password"
        v-model="password"
        required
        type="password"
        :label="$gettext('Password')"
        icon="key"
      />

      <div class="has-text-weight-bold is-centered has-text-centered mb-1" v-translate>
        Beware of case-sensitive login and password
      </div>

      <div class="buttons is-centered">
        <button type="submit" class="button is-primary" :class="{ 'is-loading': promise.loading }" v-translate>
          Login
        </button>
        <button type="button" class="button is-warning" @click="mode = 'resetPassword'" v-translate>
          Forgot password?
        </button>
        <button type="button" class="button is-link" @click="mode = 'signup'" v-translate>No account yet?</button>
      </div>
    </base-form>

    <base-form v-show="mode == 'signup'" :promise="promise" @submit="signup">
      <form-field
        ref="signupMainInput"
        name="name"
        v-model="name"
        type="text"
        :label="$gettext('Fullname')"
        icon="user-check"
      />
      <form-field
        name="username"
        v-model="username"
        type="text"
        autocapitalize="off"
        autocorrect="off"
        :label="$gettext('Username')"
        icon="user"
      />
      <form-field
        name="forum_username"
        v-model="forum_username"
        type="text"
        :label="$gettext('Forum username')"
        icon="comments"
      />
      <form-field name="password" v-model="password" type="password" :label="$gettext('Password')" icon="key" />
      <form-field name="email" v-model="email" type="email" :label="$gettext('Email')" icon="at" />
      <div class="field">
        <div class="control">
          <label class="checkbox">
            <input type="checkbox" v-model="termsAgreed" />
            &nbsp;
            <span v-translate> I have read and agree to the terms of use </span>
            <span> (</span>
            <router-link :to="{ name: 'article', params: { id: 106731 } }" v-translate> link </router-link>
            <span>).</span>
          </label>
        </div>
      </div>

      <div class="field">
        <vue-recaptcha
          ref="recaptcha"
          :sitekey="$options.recaptchaKey"
          @expired="onCaptchaExpired"
          @verify="onCaptchaVerify"
        />
      </div>

      <div class="buttons is-centered">
        <button
          type="submit"
          class="button is-primary"
          :class="{ 'is-loading': promise.loading }"
          :disabled="!termsAgreed || !captcha"
          v-translate
        >
          Register
        </button>
        <button type="button" class="button is-link" @click="mode = 'signin'" v-translate>Have an account?</button>
      </div>
    </base-form>

    <base-form ref="resetPasswordForm" v-show="mode == 'resetPassword'" :promise="promise" @submit="resetPassword">
      <h3 slot="header" class="title is-3" v-translate>Reset password</h3>

      <form-field
        ref="resetPasswordMainInput"
        name="email"
        v-model="email"
        type="email"
        :label="$gettext('Email')"
        icon="at"
      />

      <div class="buttons is-centered">
        <button type="submit" class="button is-link" :class="{ 'is-loading': promise.loading }" v-translate>
          Send reset email
        </button>
        <button type="button" class="button is-link" @click="mode = 'signin'" v-translate>Login</button>
      </div>

      <div v-if="promise.success" class="notification is-info" v-translate>
        We sent you an email, please click on the link to reset password.
      </div>
    </base-form>

    <base-form
      ref="changePasswordForm"
      v-show="mode == 'changePassword'"
      :promise="promise"
      @submit="validateNewPassword"
    >
      <h3 slot="header" class="title is-3" v-translate>Change password</h3>

      <form-field
        ref="changePasswordMainInput"
        name="password"
        v-model="password"
        type="password"
        :label="$gettext('New password')"
        icon="key"
      />

      <div class="buttons is-centered">
        <button type="submit" class="button is-link" :class="{ 'is-loading': promise.loading }" v-translate>
          Change password
        </button>
        <button type="button" class="button is-link" @click="mode = 'signin'" v-translate>Cancel</button>
      </div>
    </base-form>

    <base-form v-show="mode == 'changeEmail' || mode == 'validateAccountCreation'" :promise="promise">
      <div v-if="promise.loading" v-translate>Checking...</div>
    </base-form>
  </div>
</template>

<script>
import { toast } from 'bulma-toast';

import BaseForm from './utils/BaseForm';
import FormField from './utils/FormField';

import c2c from '@/js/apis/c2c';
import config from '@/js/config';

// possible mode values :
//
// * sigin, default : sign in with your account
// * signup : create account
// * resetPassword : get a mail with an secret URL to reset your password
// * changePassword : with url from precedent mode, set a new password
// * changeEmail : if user has asked a new mail, a secret url has been sent
// * validateAccountCreation : idem, but when account is created

export default {
  recaptchaKey: config.urls.recaptchaKey,

  components: {
    FormField,
    BaseForm,
    VueRecaptcha: () => import(/* webpackChunkName: "captcha" */ 'vue-recaptcha'),
  },

  // here is the trick : all auth action are on the same component.
  // vue won't reload it, even on route modification.
  // watch on $route will perform any action needed by url state.
  // but this function will be called only once : at the very first load of component
  // so we'll keep the page to go back
  // that's all !
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.from = from;
    });
  },

  data() {
    return {
      mode: '',

      username: '',
      password: '',
      name: '',
      forum_username: '',
      email: '',
      recaptchaAvailable: false,
      captcha: null,

      termsAgreed: false,

      from: null,
      redirectionStillDone: false,

      promise: {},
    };
  },

  computed: {},

  watch: {
    $route: 'load',
    mode: 'onModeChange',
  },

  created() {
    if (this.$route.name === 'auth-sso') {
      if (this.$route.query.logout !== undefined) {
        this.$user.signout();
      }
    }
  },

  mounted() {
    const recaptchaScript = document.createElement('script');
    recaptchaScript.async = true;
    recaptchaScript.setAttribute(
      'src',
      'https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit'
    );
    document.head.appendChild(recaptchaScript);

    this.load();
  },

  methods: {
    onModeChange() {
      this.promise = {};

      if (this.mode === 'signin') {
        this.$nextTick(this.$refs.signinMainInput.focus);
      } else if (this.mode === 'changePassword') {
        this.$nextTick(this.$refs.changePasswordMainInput.focus);
      } else if (this.mode === 'resetPassword') {
        this.$nextTick(this.$refs.resetPasswordMainInput.focus);
      } else if (this.mode === 'signup') {
        this.$nextTick(this.$refs.signupMainInput.focus);
      }
    },

    load() {
      if (this.$route.hash) {
        // keep compatible with v6 AngularJs hacks...
        this.$router.replace(this.$route.fullPath.replace('#', '?'));
      }

      if (this.$route.query.change_password) {
        // change password mode
        // mode when user has forgotten his password.
        // an url is sent to his mail, with an secret param
        this.mode = 'changePassword';
      } else if (this.$route.query.validate_change_email) {
        // when user changes his email.
        // he receives on his new mail a secret url to validate
        // that  he is the owner
        this.mode = 'changeEmail';
        this.promise = c2c.userProfile
          .validateChangeEmail(this.$route.query.validate_change_email)
          .then(() => this.$router.push({ name: 'home' }));
      } else if (this.$route.query.validate_register_email) {
        // after account creation
        this.mode = 'validateAccountCreation';
        this.promise = c2c.userProfile
          .validateRegisterEmail(this.$route.query.validate_register_email)
          .then(() => this.$router.push({ name: 'home' }));
      } else {
        this.mode = 'signin';
      }
    },

    signin() {
      this.promise = this.$user.signIn(this.username, this.password).then(this.onSucessSigin);
    },

    onSucessSigin(data) {
      const discourse_url = data.data.redirect_internal;

      if (discourse_url) {
        // dirty way to SSO...
        // if somebody wants to implement a better solution, feel free
        // https://github.com/c2corg/v6_ui/blob/c9962a6c3bac0670eab732d563f9f480379f84d1/c2corg_ui/static/js/auth/auth.js
        const iframe = document.createElement('iframe');
        const sandbox = document.createAttribute('sandbox');

        sandbox.value = 'allow-same-origin';
        iframe.style.display = 'none';
        iframe.setAttributeNode(sandbox);
        iframe.src = discourse_url;

        // 10s to complete discourse authentication
        window.setTimeout(this.redirect, 10000);
        iframe.addEventListener('load', this.redirect);

        this.promise.loading = true;
        document.body.appendChild(iframe);
      } else {
        this.redirect();
      }
    },

    redirect() {
      // redirect() may be called twice
      if (!this.redirectionStillDone) {
        this.redirectionStillDone = true;
        this.$router.push(this.from.fullPath);
      }
    },

    signup() {
      this.promise = c2c.userProfile.register({
        name: this.name,
        username: this.username,
        forum_username: this.forum_username,
        password: this.password,
        email: this.email,
        lang: this.$language.current,
        captcha: this.captcha,
      });

      this.captcha = null;
      this.$refs.recaptcha.reset();
    },

    resetPassword() {
      this.promise = c2c.userProfile
        .requestPasswordChange(this.email)
        .then(() => toast({ message: this.$gettext('Mail has been sent'), type: 'is-danger' }));
    },

    validateNewPassword() {
      const password = this.password;
      const nonce = this.$route.query.change_password;

      this.promise = c2c.userProfile
        .validateNewPassword(nonce, password)
        .then(() => this.$router.push({ name: 'auth' }));
    },

    onCaptchaExpired() {
      this.$refs.recaptcha.reset();
    },

    onCaptchaVerify(captchaKey) {
      this.captcha = captchaKey;
    },
  },
};
</script>

<style lang="scss" scoped>
.login-view {
  height: 100%;
  align-items: center;
  width: 30rem;
  max-width: 100vw;
  margin: auto;

  form {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>
