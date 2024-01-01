package fr.deroffal.stravastatistics.client.auth;

import static fr.deroffal.stravastatistics.client.AccessTokenProvider.PROFILE_API_TOKEN_PROVIDER;

import com.fasterxml.jackson.annotation.JsonProperty;
import fr.deroffal.stravastatistics.client.AccessTokenProvider;
import fr.deroffal.stravastatistics.client.StravaApiConfiguration;
import fr.deroffal.stravastatistics.client.StravaApiConfiguration.ApiConfig;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
@Profile(PROFILE_API_TOKEN_PROVIDER)
class StravaAuthApi implements AccessTokenProvider {

  private final StravaApiConfiguration apiProperties;

  public StravaAuthApi(StravaApiConfiguration stravaApiConfiguration) {
    this.apiProperties = stravaApiConfiguration;
  }

  @Override
  public String getAccessToken() {
    ApiConfig apiConfig = apiProperties.getApi();
    RestClient client = RestClient.builder()
        .baseUrl(apiConfig.getUrl().toString())
        .build();

    return client.post()
        .uri(builder -> builder.path("oauth/token")
            .queryParam("client_id", apiConfig.getClientId())
            .queryParam("client_secret", apiConfig.getClientSecret())
            .queryParam("grant_type", "refresh_token")
            .queryParam("refresh_token", apiConfig.getRefreshToken())
            .build()
        )
        .header("Accept", "application/json")
        .retrieve()
        .body(OAuthToken.class)
        .accessToken();
  }

  private record OAuthToken(
      @JsonProperty("token_type") String tokenType,
      @JsonProperty("access_token") String accessToken,
      @JsonProperty("expires_at") int expiresAt,
      @JsonProperty("expires_in") int expiresIn,
      @JsonProperty("refresh_token") String refreshToken
  ) {
  }

}
