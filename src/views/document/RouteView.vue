<template>
  <div class="section has-background-white-print">
    <document-view-header :document="document" :version="version" :promise="promise" />
    <div v-if="document" class="columns is-block-print">
      <div class="column is-3 no-print">
        <map-box :document="document" @has-protection-area="hasProtectionArea = true" />
        <tool-box :document="document" v-if="!$screen.isMobile" />
      </div>

      <div class="column is-9 is-12-print">
        <!-- CONTENT -->

        <div class="box">
          <div class="columns">
            <div class="column is-4">
              <activities-field :document="document" />
              <field-view :document="document" :field="fields.route_types" />
              <field-view :document="document" :field="fields.durations" :unit="$gettext('day(s)')" />
              <field-view :document="document" :field="fields.rock_types" />
              <field-view :document="document" :field="fields.climbing_outdoor_type" />
              <field-view :document="document" :field="fields.configuration" />
              <field-view :document="document" :field="fields.slackline_type" />
            </div>

            <div class="column is-4">
              <label-value :label="$gettext('ratings')">
                <document-rating v-if="$documentUtils.hasRating(document)" :document="document" show-helper />
                <edit-link v-else :document="document" :lang="$user.lang" />
              </label-value>

              <field-view v-if="document.glacier_gear != 'no'" :document="document" :field="fields.glacier_gear" />

              <input-orientation
                v-if="document.orientations && document.orientations.length"
                v-model="document.orientations"
                disabled
              />
            </div>

            <div class="column is-4">
              <double-numeric-field
                :document="document"
                :field1="fields.elevation_min"
                :field2="fields.elevation_max"
                :label="$gettext('elevation')"
              />

              <double-numeric-field
                :document="document"
                :field1="fields.height_diff_up"
                :field2="fields.height_diff_down"
                :label="$gettext('height_diff')"
                show-signs
              />

              <field-view :document="document" :field="fields.height_diff_difficulties" />
              <field-view :document="document" :field="fields.difficulties_height" />

              <field-view :document="document" :field="fields.height_diff_access" />
              <field-view :document="document" :field="fields.lift_access" />

              <field-view :document="document" :field="fields.route_length" :divisor="1000" unit="km" />

              <field-view :document="document" :field="fields.mtb_height_diff_portages" />
              <field-view :document="document" :field="fields.mtb_length_asphalt" :divisor="1000" unit="km" />
              <field-view :document="document" :field="fields.mtb_length_trail" :divisor="1000" unit="km" />

              <label-value v-if="document.cooked.slope" :label="$gettext('slope')">
                {{ document.cooked.slope }}
              </label-value>

              <field-view :document="document" :field="fields.slackline_height" />
            </div>
          </div>
        </div>

        <div class="box">
          <markdown-section :document="document" :field="fields.summary" />
          <markdown-section v-if="locale.route_history" :document="document" :field="fields.route_history" />
          <div v-else-if="showMissingHistoryBanner" class="notification is-info no-print missing-history-banner">
            <edit-link :document="document" :lang="lang" show-always v-translate>
              History is missing, please provide it if you have information.
            </edit-link>
          </div>
          <markdown-section :document="document" :field="fields.description" />
          <markdown-section :document="document" :field="fields.slackline_anchor1" />
          <markdown-section :document="document" :field="fields.slackline_anchor2" />

          <markdown-section :document="document" :field="fields.remarks">
            <div slot="after" v-if="hasProtectionArea" class="notification is-info protection-area-info no-print">
              <strong v-translate>Sensitive areas</strong>
              <p v-translate>There are sensitive areas on this route. Please refer to the map.</p>
            </div>
          </markdown-section>

          <markdown-section :document="document" :field="fields.gear">
            <div class="content automatic-gears" slot="after" v-if="Object.keys(gear_articles).length !== 0">
              <ul>
                <li v-for="(label, articleId) of gear_articles" :key="articleId">
                  <router-link :to="{ name: 'article', params: { id: articleId } }">
                    {{ label }}
                  </router-link>
                </li>
              </ul>
            </div>
          </markdown-section>

          <markdown-section :document="document" :field="fields.external_resources" />

          <div style="clear: both" />
        </div>

        <routes-box :document="document" hide-buttons disable-activity-split />
        <images-box :document="document" />

        <recent-outings-box :document="document" />

        <tool-box :document="document" v-if="$screen.isMobile" />

        <comments-box :document="document" />
      </div>
    </div>
  </div>
</template>

<script>
import documentViewMixin from './utils/document-view-mixin';
const historyWorthActivities = [
  'snow_ice_mixed',
  'mountain_climbing',
  'rock_climbing',
  'ice_climbing',
  'via_ferrata',
  'slacklining',
];
export default {
  mixins: [documentViewMixin],

  data() {
    return {
      hasProtectionArea: false,
    };
  },

  computed: {
    // https://github.com/c2corg/v6_ui/blob/master/c2corg_ui/templates/utils/__init__.py#L103
    gear_articles() {
      const result = {};
      const doc = this.document;
      const activities = doc.activities ?? [];
      const easy_mountain = ['F', 'F+', 'PD-', 'PD', 'PD+', 'AD-', 'AD'];
      const poor_equiped = ['P2', 'P2+', 'P3', 'P3+', 'P4'];
      const glacier_activities = ['mountain_climbing', 'skitouring', 'snow_ice_mixed', 'snowshoeing'];

      if (activities.includes('snowshoeing') || activities.includes('skitouring')) {
        result['183333'] = this.$gettext('skitouring gear');
      }

      if (activities.includes('snow_ice_mixed') && ['F', 'F+', 'PD-', 'PD', 'PD+'].includes(doc.global_rating)) {
        result['185750'] = this.$gettext('easy snow ice mixed gear');
      }

      if (activities.includes('mountain_climbing') && easy_mountain.includes(doc.global_rating)) {
        result['185384'] = this.$gettext('easy mountain climbing gear');
      }

      if (activities.includes('rock_climbing')) {
        if (['P1', 'P1+'].includes(doc.equipment_rating)) {
          result['183332'] = this.$gettext('bolted rock climbing gear');
        } else if (
          !activities.includes('mountain_climbing') &&
          easy_mountain.includes(doc.global_rating) &&
          poor_equiped.includes(doc.equipment_rating)
        ) {
          result['185384'] = this.$gettext('easy mountain climbing gear');
        }
      }

      if (activities.includes('ice_climbing')) {
        result['194479'] = this.$gettext('ice and dry climbing gear');
      }

      if (activities.includes('hiking')) {
        result['185207'] = this.$gettext('hiking gear');
      }

      // we should use an anchor for glacier gear, but it's not possible
      if (doc.glacier_gear && doc.glacier_gear !== 'no') {
        if (activities.filter((act) => glacier_activities.includes(act))) {
          result['185750'] = this.$gettext('easy snow ice mixed gear');
        }
      }

      return result;
    },

    showMissingHistoryBanner() {
      const doc = this.document;
      const activities = doc.activities ?? [];
      for (let act of historyWorthActivities) {
        if (activities.includes(act)) {
          return true;
        }
      }
      if (activities.includes('skitouring') && ['5.1', '5.2', '5.3', '5.4', '5.5'].includes(doc.ski_rating)) {
        return true;
      }
      return false;
    },
  },
};
</script>

<style lang="scss" scoped>
.missing-history-banner {
  overflow: hidden;
}

.protection-area-info {
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.automatic-gears {
  margin-bottom: 1.5rem;
}
@media print {
  .protection-area-info {
    margin: 0rem !important;
    padding: 0rem !important;
  }
}
</style>
