<template>
  <edition-container :mode="mode" :document="document" :is-loading="saving" @save="save">
    <form-section
      :title="$gettext('general informations')"
      :sub-title="$gettext('Main informations about your outing')"
    >
      <div class="columns">
        <form-field
          class="is-narrow"
          :document="document"
          :field="fields.date_start"
          :max="showBothDates ? document.date_end : undefined"
          @input="handleDates"
        />
        <form-field
          class="is-narrow"
          v-show="showBothDates"
          :document="document"
          :field="fields.date_end"
          :min="showBothDates ? document.date_start : undefined"
        />
        <div class="column is-narrow">
          <input-checkbox v-model="showBothDates">{{ $gettext('Several days?') }}</input-checkbox>
        </div>
      </div>
      <div class="columns">
        <form-field :document="document" :field="fields.activities" />
      </div>
      <map-input-row :document="document" geom-detail-editable />

      <associations-input-row :label="$gettext('routes')" :document="document" :field="fields.routes" />

      <div class="columns is-multiline">
        <form-field :document="document" :field="fields.title" />
        <form-field class="is-narrow" :document="document" :field="fields.partial_trip" />
        <form-field
          class="is-12"
          :document="document"
          :field="fields.route_description"
          :placeholder="$gettext('describe route_conditions')"
        />
      </div>
    </form-section>

    <form-section
      :title="$gettext('Weather & conditions')"
      :sub-title="$gettext('Describe the conditions you encountered during your outing')"
    >
      <div class="columns is-multiline">
        <form-field class="is-6" :document="document" :field="fields.condition_rating" />
        <form-field class="is-6" :document="document" :field="fields.glacier_rating" />
        <form-field class="is-12" :document="document" :field="fields.conditions_levels" />
      </div>
      <div class="columns">
        <form-field :document="document" :field="fields.elevation_up_snow" />
        <form-field :document="document" :field="fields.elevation_down_snow" />
      </div>
      <div class="columns">
        <form-field :document="document" :field="fields.snow_quantity" />
        <form-field :document="document" :field="fields.snow_quality" />
      </div>
      <div class="columns is-multiline">
        <form-field
          class="is-12"
          :document="document"
          :field="fields.conditions"
          :placeholder="$gettext('describe conditions')"
        />
        <form-field
          class="is-6"
          :document="document"
          :field="fields.weather"
          :placeholder="$gettext('describe weather')"
        />
        <form-field
          class="is-6"
          :document="document"
          :field="fields.timing"
          :placeholder="$gettext('describe timing')"
        />
        <form-field class="is-12" :document="document" :field="fields.avalanche_signs" />
        <form-field class="is-12" :document="document" :field="fields.avalanches" />
      </div>
    </form-section>

    <form-section
      :title="$gettext('Personal informations')"
      :sub-title="$gettext('People who were with you, and your feelings about this outing')"
    >
      <associations-input-row :label="$gettext('participants')" :document="document" :field="fields.users" />
      <div class="columns">
        <form-field :document="document" :field="fields.participant_count" class="is-narrow" />
        <form-field :document="document" :field="fields.participants" :placeholder="$gettext('Without c2c account')" />
      </div>
      <div class="columns is-multiline">
        <form-field
          class="is-12"
          :document="document"
          :field="fields.description"
          :label="$gettext('personal comments')"
          :placeholder="$gettext('write your comments')"
        />
        <form-field :document="document" :field="fields.disable_comments" />
      </div>
    </form-section>

    <form-section
      :title="$gettext('Details')"
      :sub-title="$gettext('Detailed figures, like ratings, height differences, frequentation...')"
    >
      <div class="columns">
        <form-field class="is-4" :document="document" :field="fields.frequentation" />
      </div>

      <div class="columns is-multiline">
        <div class="column is-4">
          <form-field no-wrapper :document="document" :field="fields.elevation_access" />
          <form-field no-wrapper :document="document" :field="fields.access_condition" />
          <form-field no-wrapper :document="document" :field="fields.public_transport" />
        </div>
        <form-field class="is-8" :document="document" :field="fields.access_comment" />

        <div class="column is-4">
          <form-field no-wrapper :document="document" :field="fields.lift_status" />
          <form-field no-wrapper :document="document" :field="fields.hut_status" />
        </div>
        <form-field class="is-8" :document="document" :field="fields.hut_comment" />
      </div>

      <div class="columns">
        <form-field class="is-4" :document="document" :field="fields.height_diff_up" />
        <form-field class="is-4" :document="document" :field="fields.height_diff_down" />
        <form-field class="is-4" :document="document" :field="fields.height_diff_difficulties" />
      </div>

      <div class="columns">
        <form-field class="is-4" :document="document" :field="fields.length_total" unit="km" :divisor="1000" />
        <form-field class="is-4" :document="document" :field="fields.elevation_min" />
        <form-field class="is-4" :document="document" :field="fields.elevation_max" />
      </div>

      <div class="columns is-multiline">
        <form-field class="is-4" :document="document" :field="fields.global_rating" />
        <form-field class="is-4" :document="document" :field="fields.rock_free_rating" />
        <form-field class="is-4" :document="document" :field="fields.engagement_rating" />
        <form-field class="is-4" :document="document" :field="fields.equipment_rating" />

        <!-- TODO cotometer -->
        <form-field
          class="is-4"
          :document="document"
          :field="fields.ski_rating"
          prefix="?"
          @click-prefix="showCotometer"
        />
        <form-field class="is-4" :document="document" :field="fields.labande_global_rating" />

        <form-field class="is-4" :document="document" :field="fields.ice_rating" />
        <form-field class="is-4" :document="document" :field="fields.snowshoe_rating" />
        <form-field class="is-4" :document="document" :field="fields.via_ferrata_rating" />
        <form-field class="is-4" :document="document" :field="fields.hiking_rating" />
      </div>

      <div class="columns">
        <form-field class="is-4" :document="document" :field="fields.mtb_down_rating" />
        <form-field class="is-4" :document="document" :field="fields.mtb_up_rating" />
      </div>

      <div class="columns">
        <quality-field ref="qualityField" class="is-4" :document="document" />
      </div>
    </form-section>

    <!-- TODO where is that ??
            <form-field :document="document" :field="fields.summary"/>
        -->
    <cotometer-window ref="cotometerWindow" v-if="document" v-model="document.ski_rating" />
  </edition-container>
</template>

<script>
import CotometerWindow from './utils/CotometerWindow';
import documentEditionViewMixin from './utils/document-edition-view-mixin';

export default {
  components: { CotometerWindow },

  mixins: [documentEditionViewMixin],

  data() {
    return {
      showBothDates: false,
    };
  },

  watch: {
    showBothDates: 'handleDates',
  },

  methods: {
    afterLoad() {
      this.showBothDates = this.document.date_start !== this.document.date_end;
    },

    handleDates() {
      if (!this.showBothDates) {
        this.document.date_end = this.document.date_start;
      }
    },

    beforeSave() {
      this.handleDates();
      this.$refs.qualityField.beforeSave();
    },

    showCotometer() {
      this.$refs.cotometerWindow.show();
    },
  },
};
</script>
