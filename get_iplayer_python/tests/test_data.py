episode_playlist_json = {"info":{"readme":"For the use of Radio, Music and Programmes only"},"statsObject":{"parentPID":"m000669y","parentPIDType":"episode"},"defaultAvailableVersion":{"pid":"m000669t","types":["Original"],"smpConfig":{"title":"Diplo and Friends, distinkt in the mix","summary":"distinkt in the mix exclusively for Diplo and friends - only on 1Xtra and Radio 1.","masterBrandName":"BBC Radio 1","items":[{"vpid":"m000669t","kind":"radioProgramme","duration":3600}],"holdingImageURL":"\/\/ichef.bbci.co.uk\/images\/ic\/$recipe\/p07f0n8q.jpg","guidance":"Contains language which some may find offensive.","embedRights":"blocked"},"markers":[]},"allAvailableVersions":[{"pid":"m000669t","types":["Original"],"smpConfig":{"title":"Diplo and Friends, distinkt in the mix","summary":"distinkt in the mix exclusively for Diplo and friends - only on 1Xtra and Radio 1.","masterBrandName":"BBC Radio 1","items":[{"vpid":"m000669t","kind":"radioProgramme","duration":3600}],"holdingImageURL":"\/\/ichef.bbci.co.uk\/images\/ic\/$recipe\/p07f0n8q.jpg","guidance":"Contains language which some may find offensive.","embedRights":"blocked"},"markers":[]}],"holdingImage":"\/\/ichef.bbci.co.uk\/images\/ic\/976x549\/p07f0n8q.jpg"}


mpd_file = """
<?xml version="1.0" encoding="utf-8"?>
<!-- Created with Unified Streaming Platform(version=1.7.32) -->
<MPD
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="urn:mpeg:dash:schema:mpd:2011"
  xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd"
  type="static"
  mediaPresentationDuration="PT1H59M59.844375S"
  maxSegmentDuration="PT7S"
  minBufferTime="PT3.200S"
  profiles="urn:dvb:dash:profile:dvb-dash:2014,urn:dvb:dash:profile:dvb-dash:isoff-ext-live:2014">
  <Period
    id="1"
    duration="PT1H59M59.844375S">
    <BaseURL>dash/</BaseURL>
    <AdaptationSet
      group="1"
      contentType="audio"
      lang="en"
      minBandwidth="128000"
      maxBandwidth="320000"
      segmentAlignment="true"
      audioSamplingRate="48000"
      mimeType="audio/mp4"
      codecs="mp4a.40.2"
      startWithSAP="1">
      <AudioChannelConfiguration
        schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011"
        value="2">
      </AudioChannelConfiguration>
      <Role schemeIdUri="urn:mpeg:dash:role:2011" value="main" />
      <SegmentTemplate
        timescale="48000"
        duration="307200"
        initialization="vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$.dash"
        media="vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$-$Number$.m4s">
      </SegmentTemplate>
      <Representation
        id="audio_eng=128000"
        bandwidth="128000">
      </Representation>
      <Representation
        id="audio_eng=320000"
        bandwidth="320000">
      </Representation>
    </AdaptationSet>
    <AdaptationSet
      group="1"
      contentType="audio"
      lang="en"
      minBandwidth="48000"
      maxBandwidth="96000"
      segmentAlignment="true"
      audioSamplingRate="48000"
      mimeType="audio/mp4"
      codecs="mp4a.40.5"
      startWithSAP="1">
      <AudioChannelConfiguration
        schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011"
        value="2">
      </AudioChannelConfiguration>
      <Role schemeIdUri="urn:mpeg:dash:role:2011" value="main" />
      <SegmentTemplate
        timescale="48000"
        duration="307200"
        initialization="vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$.dash"
        media="vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2-$RepresentationID$-$Number$.m4s">
      </SegmentTemplate>
      <Representation
        id="audio_eng_1=48000"
        bandwidth="48000">
      </Representation>
      <Representation
        id="audio_eng_1=96000"
        bandwidth="96000">
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
"""

dash_json = """
{"media":[{"bitrate":"320","service":"[deprecated]","kind":"audio","type":"audio/mp4","encoding":"aac","expires":"2019-07-29T05:00:00Z","connection":[{"priority":"20","protocol":"http","authExpiresOffset":21600,"supplier":"mf_akamai_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"http://aod-dash-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_dash_master.mpd?__gda__=1561417917_fe6679f6d0049efaf5fc5fff57a89b30","transferFormat":"dash","dpw":"50"},{"priority":"20","protocol":"https","authExpiresOffset":21600,"supplier":"mf_akamai_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"https://aod-dash-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_dash_master.mpd?__gda__=1561417917_fe6679f6d0049efaf5fc5fff57a89b30","transferFormat":"dash","dpw":"50"},{"priority":"30","protocol":"http","authExpiresOffset":21600,"supplier":"mf_limelight_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"http://aod-dash-uk-live.bbcfmt.hs.llnwd.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_dash_master.mpd?s=1561374717&e=1561417917&h=5678a5e93eb589bdbedb0117dbd8d6c8","transferFormat":"dash","dpw":"50"},{"priority":"30","protocol":"https","authExpiresOffset":21600,"supplier":"mf_limelight_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"https://aod-dash-uk-live.bbcfmt.hs.llnwd.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_dash_master.mpd?s=1561374717&e=1561417917&h=89a611c544ad07d5703849d8d2950bb6","transferFormat":"dash","dpw":"50"},{"priority":"20","protocol":"http","authExpiresOffset":21600,"supplier":"mf_akamai_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"http://aod-hds-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_hds_master.f4m?__gda__=1561417917_a3124c47d139dfd715c8e2eecb6e345f","transferFormat":"hds","dpw":"50"},{"priority":"20","protocol":"https","authExpiresOffset":21600,"supplier":"mf_akamai_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"https://aod-hds-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_hds_master.f4m?__gda__=1561417917_a3124c47d139dfd715c8e2eecb6e345f","transferFormat":"hds","dpw":"50"},{"priority":"30","protocol":"http","authExpiresOffset":21600,"supplier":"mf_limelight_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"http://aod-hds-uk-live.bbcfmt.hs.llnwd.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_hds_master.f4m?s=1561374717&e=1561417917&h=5db3b1247204e5d21c7a7dfe0f75bee5","transferFormat":"hds","dpw":"50"},{"priority":"30","protocol":"https","authExpiresOffset":21600,"supplier":"mf_limelight_nonbidi","authExpires":"2019-06-24T23:11:57Z","href":"https://aod-hds-uk-live.bbcfmt.hs.llnwd.net/usp/auth/vod/piff_abr_full_audio/c0289f-m000669t/vf_m000669t_ebc9f7bb-7a21-409a-a38f-f9943afbe1be.ism/pc_hd_abr_v2_uk_hds_master.f4m?s=1561374717&e=1561417917&h=57febcd5ce7a5751ffcf170c4cdae60b","transferFormat":"hds","dpw":"50"}]}],"disclaimer":"This code and data form part of the BBC iPlayer content protection system. Tampering with, removal of, misuse of, or unauthorised use of this code or data constitutes circumvention of the BBC's content protection measures and may result in legal action. BBC (C) 2019."}
"""

dash_xml = """
<mediaSelection xmlns="http://bbc.co.uk/2008/mp/mediaselection">
<!--
This code and data form part of the BBC iPlayer content protection system. Tampering with, removal of, misuse of, or unauthorised use of this code or data constitutes circumvention of the BBC's content protection measures and may result in legal action. BBC (C) 2017.
-->
    <media bitrate="128" encoding="aac" expires="2019-07-16T00:00:00Z" kind="audio" media_file_size="116548958" service="stream-uk-audio_streaming_aac_med" type="audio/mp4">
        <connection href="http://cp143012-i.akamaihd.net/i/prod_af_mp4_aaclc_128/iplayerstream/p07cf0cn_m0005zsl_cUnknown_1560765723931.mp4/master.m3u8?hdnea=st=1561284726~exp=1561306326~acl=/*p07cf0cn_m0005zsl_cUnknown_1560765723931.mp4*~hmac=e49812cdaad92d2f8d989d69efd8a905eab3302a85930312ed3029671a3c3d52" priority="10" protocol="http" supplier="akamai_hls_open" transferFormat="hls"/>
        <connection href="https://cp143012-i.akamaihd.net/i/prod_af_mp4_aaclc_128/iplayerstream/p07cf0cn_m0005zsl_cUnknown_1560765723931.mp4/master.m3u8?hdnea=st=1561284726~exp=1561306326~acl=/*p07cf0cn_m0005zsl_cUnknown_1560765723931.mp4*~hmac=e49812cdaad92d2f8d989d69efd8a905eab3302a85930312ed3029671a3c3d52" priority="100" protocol="https" supplier="akamai_hls_open_https" transferFormat="hls"/>
    </media>
    <media bitrate="320" encoding="aac" expires="2019-07-16T00:00:00Z" kind="audio" service="stream-uk-audio_streaming_concrete_combined" type="audio/mp4">
        <connection authExpires="2019-06-23T20:15:37+00:00" authExpiresOffset="36211" href="http://aod-dash-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/9ab037-m0005zsl/vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2.ism/iptv_hd_abr_v1_uk_dash_master.mpd?__gda__=1561306326_b68637b1f22510e8100e5cee25b58dde" priority="1" protocol="http" supplier="af_akamai_uk_dash" transferFormat="dash"/>
        <connection authExpires="2019-06-23T20:06:29+00:00" authExpiresOffset="35663" href="http://aod-hls-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/9ab037-m0005zsl/vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2.ism/iptv_hd_abr_v1_uk_hls_master.m3u8?__gda__=1561306326_dc2fdd745f0d7148e95126721ea09e81" priority="1" protocol="http" supplier="af_akamai_uk_hls" transferFormat="hls"/>
        <connection authExpires="2019-06-23T20:46:41+00:00" authExpiresOffset="38075" href="https://aod-dash-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/9ab037-m0005zsl/vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2.ism/iptv_hd_abr_v1_uk_dash_master.mpd?__gda__=1561306326_b68637b1f22510e8100e5cee25b58dde" priority="10" protocol="https" supplier="af_akamai_uk_dash_https" transferFormat="dash"/>
        <connection authExpires="2019-06-23T19:29:40+00:00" authExpiresOffset="33454" href="https://aod-hls-uk-live.akamaized.net/usp/auth/vod/piff_abr_full_audio/9ab037-m0005zsl/vf_m0005zsl_bba0ebc7-4603-4db7-bc26-3a84f62df2f7.ism.hlsv2.ism/iptv_hd_abr_v1_uk_hls_master.m3u8?__gda__=1561306326_dc2fdd745f0d7148e95126721ea09e81" priority="10" protocol="https" supplier="af_akamai_uk_hls_https" transferFormat="hls"/>
    </media>
</mediaSelection>
"""

metadata_json = {
    "programme": {
        "type": "episode",
        "pid": "m000669y",
        "expected_child_count": None,
        "position": None,
        "image": {
            "pid": "p07dsbjv"
        },
        "media_type": "audio",
        "title": "distinkt in the mix",
        "short_synopsis": "distinkt in the mix exclusively for Diplo and friends - only on 1Xtra and Radio 1.",
        "medium_synopsis": "distinkt in the mix exclusively for Diplo and friends - only on 1Xtra and Radio 1... Expect new music from the likes of IAMDDB, Anti Up, AJ Tracey, Randomer and loads more!",
        "long_synopsis": "distinkt in the mix exclusively for Diplo and friends - only on 1Xtra and Radio 1... Expect brand new and exclusive music from the likes of IAMDDB, Anti Up, AJ Tracey, Randomer and loads more!",
        "first_broadcast_date": "2019-06-23T00:00:00+01:00",
        "display_title": {
            "title": "Diplo and Friends",
            "subtitle": "distinkt in the mix"
        },
        "parent": {
            "programme": {
                "type": "brand",
                "pid": "b01dmw90",
                "title": "Diplo and Friends",
                "short_synopsis": "Diplo and friends exclusively in the mix - only on 1Xtra and Radio 1.",
                "media_type": None,
                "position": None,
                "image": {
                    "pid": "p06r2bq5"
                },
                "expected_child_count": None,
                "first_broadcast_date": "2012-04-08T01:00:00+01:00",
                "aggregated_episode_count": 411,
                "ownership": {
                    "service": {
                        "type": "radio",
                        "id": "bbc_radio_one",
                        "key": "radio1",
                        "title": "BBC Radio 1"
                    }
                }
            }
        },
        "peers": {
            "previous": {
                "type": "episode",
                "pid": "m000669p",
                "title": "Anna Lunoe in the mix",
                "first_broadcast_date": "2019-06-22T23:00:00+01:00",
                "position": None,
                "media_type": "audio"
            },
            "next": {
                "type": "episode",
                "pid": "m0006d20",
                "title": "29/06/2019",
                "first_broadcast_date": "2019-06-29T23:00:00+01:00",
                "position": None,
                "media_type": "audio"
            }
        },
        "versions": [
            {
                "canonical": 1,
                "pid": "m000669t",
                "duration": 3600,
                "types": [
                    "Original version"
                ]
            }
        ],
        "links": [],
        "supporting_content_items": [],
        "categories": [
            {
                "type": "genre",
                "id": "C00070",
                "key": "danceandelectronica",
                "title": "Dance & Electronica",
                "narrower": [],
                "broader": {
                    "category": {
                        "type": "genre",
                        "id": "C00066",
                        "key": "music",
                        "title": "Music",
                        "broader": {},
                        "has_topic_page": False,
                        "sameAs": None
                    }
                },
                "has_topic_page": False,
                "sameAs": None
            },
            {
                "type": "genre",
                "id": "C00166",
                "key": "hiphop",
                "title": "Hip Hop",
                "narrower": [],
                "broader": {
                    "category": {
                        "type": "genre",
                        "id": "C00077",
                        "key": "hiphoprnbanddancehall",
                        "title": "Hip Hop, RnB & Dancehall",
                        "broader": {
                            "category": {
                                "type": "genre",
                                "id": "C00066",
                                "key": "music",
                                "title": "Music",
                                "broader": {},
                                "has_topic_page": False,
                                "sameAs": None
                            }
                        },
                        "has_topic_page": False,
                        "sameAs": None
                    }
                },
                "has_topic_page": False,
                "sameAs": None
            },
            {
                "type": "format",
                "id": "PT016",
                "key": "mixes",
                "title": "Mixes",
                "narrower": [],
                "broader": {},
                "has_topic_page": False,
                "sameAs": None
            }
        ]
    }
}