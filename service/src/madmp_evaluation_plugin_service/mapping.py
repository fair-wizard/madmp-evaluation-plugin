"""Mapping of FAIR Wizard projects using dsw:root knowledge model (2.7.0+) to RDA DMP Common Standard (maDMP)."""
import re
from typing import Any

SUPPORTED_KM_PREFIXES = ('dsw:root:', 'dsw:lifesciences:')


class UUIDs:
    adminDetailsCUuid = '1e85da40-bbfc-4180-903e-6c569ed2da38'
    contributorsQUuid = '73d686bd-7939-412e-8631-502ee6d9ea7b'
    contributorNameQUuid = '6155ad47-3d1e-4488-9f2a-742de1e56580'
    contributorEmailQUuid = '3a2ffc13-6a0e-4976-bb34-14ab6d938348'
    contributorOrcidQUuid = '6295a55d-48d7-4f3c-961a-45b38eeea41f'
    contributorRoleQUuid = '829dcda6-db8a-40ac-819a-92b9b52490f5'
    contributorRoleContactPersonAUuid = '2c6ee59d-4dc9-4dcb-ac13-d969c317a117'
    contributorRoleDataCollectorAUuid = 'fc789e2d-01ee-432d-82f9-1b659f58eaf8'
    contributorRoleDataCuratorAUuid = '618cb529-0c24-4762-a739-7983004d1b2b'
    contributorRoleDataManagerAUuid = '627ab8dc-8026-498d-ba7a-3df122e29ede'
    contributorRoleDataProtectorAUuid = 'bc82b138-9816-46dd-8ff8-cea2826a3ad4'
    contributorRoleDataStewardAUuid = '3022098b-0e2c-4fad-9f28-cf2e1325521d'
    contributorRoleDistributorAUuid = '27dccf06-3b67-4c75-8888-6549e4da2d31'
    contributorRoleEditorAUuid = '100daf28-b55e-4b04-8295-f2aa83d0c734'
    contributorRoleProducerAUuid = '2085d67e-e144-4ec2-a788-1b26ac1cd7ab'
    contributorRoleProjectLeaderAUuid = '2d433965-55e3-4540-aae4-f85639d4e4fc'
    contributorRoleProjectManagerAUuid = 'cd2d1e0d-c5ad-4d0e-afa2-5ed143323cb7'
    contributorRoleProjectMemberAUuid = '3d166766-6511-407b-a3e9-9565628fe05a'
    contributorRoleResearcherAUuid = 'c81c63b6-bec0-4e12-b9cd-247fa4338c1f'
    contributorRoleRightsHolderAUuid = '704ebc65-6932-4679-bbe5-f25c19843f0f'
    contributorRoleSponsorAUuid = '374b887f-dfd8-4763-b360-b2a8aa12051c'
    contributorRoleSupervisorAUuid = '6dfde2b6-4234-47a0-b7da-ccb7412f8490'
    contributorRoleWorkPackageLeaderAUuid = 'ce5476ed-5cc3-42ff-ac9d-d567f28cc2a6'
    contributorRoleWorkCreatorOfDMPAUuid = '21047dec-71ee-40e4-868a-3ed75a027ff6'
    contributorRoleOtherAUuid = 'e957ecd5-baa2-4a3c-aaf1-735d416e5e11'
    projectsQUuid = 'c3dabaaf-c946-4a0d-889c-ede966f97667'
    projectNameQUuid = 'f0ef08fd-d733-465c-bc66-5de0b826c41b'
    projectAbstractQUuid = '22583d74-3c98-4e0a-b363-26d767c88212'
    projectStartQUuid = 'de84b9b5-bcd0-4954-8370-72ea83916b8c'
    projectEndQUuid = 'cabc6f07-6015-454e-b97a-c34db4ec0c60'
    costQUuid = '353eeaca-45fa-4958-a33c-ec6de3075701'
    costTitleQUuid = '7098b454-bc5e-4f83-a95d-970aa42e1479'
    costDescriptionQUuid = 'b3d9b6ca-bd24-4fa3-a3bd-d15005b9ae8b'
    costCurrencyQUuid = 'ac1f8f04-17a2-49e9-b2ad-2a9f8e44efb3'
    costAmountQUuid = 'e53fdad9-7799-4eb4-8b4d-fa9aa05f9d2d'
    costAllocationQUuid = '028909e8-7392-4385-96a3-467d79c43a42'
    costAllocationFindabilityAUuid = 'd84664d4-9bb6-40ff-bde5-3c1ed58ce522'
    costAllocationAccessibilityAUuid = '9ffe7d27-a04c-481e-8e20-09b6afd8fabf'
    costAllocationInteroperabilityAUuid = '8258c093-d1c8-4d41-801e-44e2c8ce6c86'
    costAllocationReusabilityAUuid = '350a6e85-d4b2-4a44-831d-4562e5668208'
    costManagementAUuid = 'd2a9d717-c0b2-44ee-8a6d-8476831b6225'
    projectFundingQUuid = '36a87eac-402d-43fb-a0df-ac5963bdf87d'
    projectFundingFunderQUuid = '0b12fb8c-ee0f-40c0-9c53-b6826b786a0c'
    projectFundingStatusQUuid = '54ff3b18-652f-4235-8f9f-3c87e2d63169'
    projectFundingStatusPlannedAUuid = '59ed0193-8211-4ee8-8d36-0640d99ce870'
    projectFundingStatusAppliedAUuid = '85fad342-a89d-414b-bc83-286a7417bb78'
    projectFundingStatusGrantedAUuid = 'dcbeab22-d188-4fa0-b50b-5c9d1a2fbefe'
    projectFundingStatusRejectedAUuid = '8c0c9f28-4672-46ba-a939-48c2c892d790'
    projectFundingGrantNumberQUuid = '1ccbd0bb-4263-4240-9dc5-936ef09eef53'
    reusingCUuid = '82fd0cce-2b41-423f-92ad-636d0872045c'
    preexistingQUuid = 'efc80cc8-8318-4f8c-acb7-dc1c60e491c1'
    preexistingYesAUuid = '2663b978-5125-4224-9930-0a50dbe895c9'
    nrefDataQUuid = 'be872000-cb98-442f-999c-ca3ef58dcfe8'
    nrefDataNameQUuid = '682da8d1-c109-4f62-8cf1-dadd8908af77'
    nrefDataWhereQUuid = '5f73797c-268a-4862-b48b-75719ff47709'
    nrefDataUseQUuid = 'f5e129dc-d59d-4352-a5ed-25efe1d83811'
    nrefDataUseYesAUuid = '7fc8d3c9-a2d5-4d47-9df4-56af48ca85e1'
    nrefDataPersonalQUuid = '50864250-7dad-421a-9f6c-303114fe6e6c'
    nrefDataPersonalNoAUuid = '381058ff-8fed-40f5-928e-06e19e90dd1c'
    nrefDataPersonalYesAUuid = '1bbafc04-e527-481b-ad1f-521cc48de186'
    nrefDataPersonalLegalBasisQUuid = 'c2da0410-ede1-4b0a-a750-09e6e6bd38cf'
    nrefDataPersonalLegalBasisPublicInAUuid = '597d2547-4e97-4045-8605-3b5249f2b412'
    nrefDataPersonalLegalBasisConsentAUuid = 'eb17ff9a-c57e-4fd4-b3bd-89edb31c6568'
    nrefDataPersonalConsentReuseQUuid = '28e7c4f7-7ade-42b2-a68e-63ab4f67b960'
    nrefDataPersonalConsentReuseYesAUuid = '15071f5e-c120-4a10-b0e8-054dea4dbf04'
    nrefDataPersonalConsentReuseNoAUuid = '5374139c-f125-4d04-bce2-3ef6d4b34a2a'
    nrefDataPersonalLegalBasisOtherAUuid = 'ef396bbf-daa7-4d61-b4d7-ab66900b2598'
    nrefDataPersonalLegalBasisOtherQUuid = '40ea30cc-ea49-4407-8bba-c511a9fb1786'
    nrefDataPersonalLegalBasisLegReqAUuid = '18db88c7-97c9-416e-b1ae-763bf018345e'
    nrefDataPersonalLegalBasisVitInterAUuid = '8caeb960-7c5e-457c-ae9e-1a2e038a466a'
    nrefDataPersonalLegalBasisLegInterAUuid = '34bf8a67-6bba-4eab-8264-8d76f97e66c8'
    nrefDataPersonalLegalBasisContractAUuid = 'bfb7a92c-5eec-497e-8a0f-ef7b12f353c2'
    nrefDataEthicalAppQUuid = 'c15710f6-1c7f-43a0-97e7-ab70f6b5a115'
    nrefDataEthicalAppCoversAUuid = '284110a8-66b4-4ba5-9e7a-edb77b1f2b3a'
    nrefDataEthicalAppExtensionAUuid = '12ae8bdc-a6eb-4db9-9a1a-7e6fed7f9ace'
    nrefDataEthicalAppNewAUuid = '6dd1142d-f76f-4d0b-9c38-999f7d8a229b'
    creatingCUuid = 'b1df3c74-0b1f-4574-81c4-4cc2d780c1af'
    collectPersonalQUuid = '49c009cb-a38c-4836-9780-8a8b3dd1cbac'
    collectPersonalNoAUuid = '4bdc319d-282a-4a80-9cdd-78d2081e812b'
    collectPersonalYesAUuid = '421e2d3e-c95c-4244-9465-de8f1cb8aeba'
    cpersGdprQUuid = 'c8687abf-ac88-4bef-b1cc-7070bd039a07'
    cpersGdprExploreAUuid = 'd8ecede2-f952-4b08-8a68-20d97849733f'
    cpersLegalBasisQUuid = 'be4651c9-9a8c-4e10-a158-61b94ca0e139'
    cpersLegalBasisAskAUuid = '73cd2dda-41ba-456b-9a4e-aa34c78f2fcf'
    cpersConsentQUuid = 'f5e162ee-1077-4ebe-a932-192bc7f67e98'
    cpersConsentUseAUuid = 'a484287c-fd7f-47ca-8dea-cdb36f48616d'
    cpersConsentReuseAUuid = '08014631-8a8a-4efa-bd58-3766cc40c7ed'
    cpersConsentUseAnonAUuid = '3a77595a-87ae-484d-a9a6-052f312453ee'
    cpersConsentAnonAUuid = 'e7e4f219-5edd-468f-b042-b5f88a559c3a'
    cpersReusersQUuid = 'd0e029ee-aee0-420f-bc6f-ad471410ad42'
    cpersReusersNoAUuid = 'e4b4093e-9abd-40ce-bd9a-8720b2966017'
    cpersReusersYesAUuid = 'dce67815-b47b-4e92-a70e-b32735cf9e5b'
    cpersLegalBasisPublicAUuid = 'c732f0b9-2f66-47f4-902f-724a44cdfd4b'
    cpersLegalBasisOtherAUuid = '2a84c15c-f5ca-4471-b1fe-10f3d1231f24'
    cpersLegalBasisOtherQUuid = 'b307cc44-7896-4383-b9b0-11cf4a58f531'
    cpersLegalBasisContractAUuid = '1dfe0a6d-4281-4d5e-bcaa-5e20fa28a591'
    cpersLegalBasisLegitAUuid = '9d5e3104-2b6b-4d95-848e-253ef069d8b3'
    cpersLegalBasisVitalAUuid = '557a5401-a94a-4a37-af2e-a21829557bfa'
    cpersLegalBasisLegalAUuid = 'f10de3a8-2751-42c7-afaa-92eed4833f8e'
    cpersNeedDpiaQUuid = '8915bd25-db22-4ed6-bcc8-b1bbdc52989e'
    cpersNeedDpiaYesAUuid = 'c3914e43-cca1-4180-8960-228b7022bae6'
    ethicsLegislationQUuid = 'ebcbf4c6-ce25-4a0b-9e82-039a88498203'
    ethicsLegislationYesAUuid = '9310b639-4cf7-4f94-8fbe-c1afc50afe4b'
    ethicsLegislationNoAUuid = '579c0a9a-29f0-4ab8-991d-bc4f55f2e4b8'
    ethicsReviewQUuid = '3782d32b-91b5-432f-8f93-92bb22868a22'
    ethicsReviewNoAUuid = '6480ac87-faaa-4b47-9a66-f338e95ace5a'
    ethicsReviewYesAUuid = '04644b31-678c-45d5-807d-93d0d79f2221'
    ethicsHumanSubjectsQUuid = 'b464593d-fb92-4ad9-88e1-764306bb3051'
    ethicsHumanSubjectsYesAUuid = '761d20f2-d2ce-496b-8a91-a52ff0513e7b'
    givingAccessCUuid = '6be88f7c-f868-460f-bba7-91e1c659adfd'
    canOpenQUuid = 'a549d10b-aa46-4c0c-863f-30219ac5ecce'
    canOpenNoAUuid = 'b3739ebd-2d8e-42d3-9425-a7d6d1b26c79'
    legalReasonsQUuid = 'c010e830-bd89-460d-9498-cb41e7ffeb87'
    legalReasonsYesAUuid = 'aac95530-2978-4759-803b-64721533faf0'
    privacyReasonsQUuid = '019db0b3-9067-4134-8bfd-76db3cfc572a'
    privacyReasonsYesAUuid = '8a56768a-5c5a-44c0-b21c-46a231fbf6be'
    privacyRestrictionsQUuid = '754148c2-6019-4318-8d44-d73becc989f4'
    privacyRestrictionsNoAUuid = '6fd34203-6217-4c1b-a706-c5fa155ea706'
    privacyRestrictionsYesEUAUuid = '2f0e4c16-be62-4836-aa0e-b52fd9132ac7'
    privacyRestrictionsYesCountryAUuid = '00bddac1-2375-4554-bb3c-27b261cc22e7'
    privacyRestrictionsYesInstituteAUuid = 'f6adfe7d-45f5-41a4-ba48-e43cc131c824'
    privacyPseudoQUuid = 'a25b30f4-2d0f-4132-9b8e-0950f0b0ed66'
    privacyPseudoNoAUuid = '5edeab6e-81a9-4209-b063-8d6fca55a388'
    privacyPseudoYesAUuid = '49f268a6-9566-4aa4-bec3-44fec2e64548'
    privacyAnonQUuid = '15ee1921-1fea-4f22-b462-b3cf7cdd4646'
    privacyAnonNoAUuid = '324dc2d9-df7f-4849-a5c0-91ecf2ef2dbd'
    privacyAnonYesAUuid = 'c0d7df59-0cf2-4ff1-9dd0-a2f2dd5bed91'
    privacyAggregationQUuid = '69be6695-152b-48ba-a1fd-6662476e39b7'
    privacyAggregationNoAUuid = '94811bac-3a00-40cd-acdf-638cd79845a8'
    privacyAggregationYesAUuid = '1c1c557c-ef6c-44ff-b618-c1cfe3543057'
    preservingCUuid = 'd5b27482-b598-4b8c-b534-417d4ad27394'
    producingQUuid = '4e0c1edf-660c-4ebf-81f5-9fa959dead30'
    producingNameQUuid = 'b0949d09-d179-4491-9fb4-14b0deb9f862'
    producingDescriptionQUuid = '205a886d-83d7-4359-ae63-7103e05357c3'
    producingTypeQUuid = '3a8ed3fc-b1a6-4119-80ed-238804861734'
    producingTypeRawAUuid = '79f7797e-f7b1-4930-b691-84bee936af20'
    producingTypeIntermediateAUuid = '5b49df5e-1d06-446f-a518-33a06928b598'
    producingTypeProcessedUnpublishableAUuid = '4fa0c31a-bd3b-4ae0-8f56-639ae2212124'
    producingTypeProcessedPublishedAUuid = '626a610e-34ac-40ca-8bf6-7926f580ae80'
    producingIdsQUuid = 'cf727a0a-78c4-45a7-aa9b-cf7650ae873a'
    producingIdsTypeQUuid = '5c22cf59-89e3-43a1-af10-1af43a97bcb2'
    producingIdsTypeHandleAUuid = 'b93a037a-006a-486f-87e0-6bef5c28879b'
    producingIdsTypeDoiAUuid = '48062bc9-0ffb-4509-bec6-e90641a30569'
    producingIdsTypeArkAUuid = 'c353f027-823b-4242-9149-37dca26cf4bc'
    producingIdsTypeUrlAUuid = '7a1d3b28-5f85-48b8-b052-2448c276d9fc'
    producingIdsTypeOtherAUuid = '97236701-7b62-40f8-99a0-3b18d3fe3658'
    producingIdsTypeNoneAUuid = '640d232f-69bc-4d4e-89ef-2d94db27f65f'
    producingIdsIdQUuid = '9e13b2d3-5f00-4e19-8a52-5c33c5b1cb07'
    producingPersonalQUuid = 'a1d76760-053c-4706-80a2-cfb6c6a061f3'
    producingPersonalNoAUuid = '4b2a08c7-4942-41fc-8114-d3868c882624'
    producingPersonalYesAUuid = '0cdc4817-7c54-4ec1-b2f4-5c007a85c7b8'
    producingSensitiveQUuid = 'cc95b399-7d8d-4232-bccf-686f78c91bff'
    producingSensitiveNoAUuid = '60de66a3-d303-4784-8931-bc58f8a3e747'
    producingSensitiveYesAUuid = '2686575d-cd74-4e2c-8524-eaca6f510425'
    keptQUuid = 'd4e6a244-07fb-4573-b93f-c20a9409ac7c'
    keptTechnicallyPossibleAUuid = '59305ef2-2dd0-4553-8d7b-29186e0b8cd5'
    keptUntilDeletedAUuid = 'bb6b4f0a-9908-4473-9982-30084ff4f6ab'
    keptFixedPeriodAUuid = '7b5f059a-ae7e-4f7f-92e8-119911e568b2'
    keptFixedPeriodHowLongQUuid = '346118ee-265f-4104-8409-161ea9a57f75'
    keptMetadataQUuid = '3b3fbcc6-c405-4151-8dce-e11dbd46b1bd'
    keptMetadataNoAUuid = 'b2eff435-ddbb-4172-a178-38aa71c700b4'
    keptMetadataYesAUuid = 'd21c32f1-c150-4c89-8472-2918d60dd547'
    publishedQUuid = 'a063da1c-aaea-4e18-85ec-f560d833f292'
    publishedYesAUuid = '8d1b07a7-f177-41f5-9532-05536223a8d6'
    distrosQUuid = '81d3095e-a530-40a4-878e-ced42fabc4cd'
    distroRepositoryQUuid = '80a682bd-8a5c-4a52-935d-680509838a4e'
    distroRepositoryDomainAUuid = '1dc412c6-da92-4cc2-8639-316c0c6ec5ff'
    distroRepositoryDomainWhichQUuid = '221c322e-dff5-438f-8a2e-90e762681156'
    distroRepositoryNationalAUuid = 'fb96d008-f31a-4a1a-b203-b3f9bb32fcc8'
    distroRepositoryInstitutionalAUuid = 'df0b2ee3-8e4d-42a1-9bb2-c69228074406'
    distroRepositorySpecialAUuid = 'afd9f4d5-20e0-4fa0-a42a-376c132ff5b0'
    distroRepositoryGeneralAUuid = 'd3886c3e-6cf7-4b3e-8bc7-307b47719871'
    distroRepositoryGeneralWhichQUuid = '371362c3-c2d1-419e-a7d6-b891a976a1fd'
    distroAccessQUuid = '82fc0a41-8be0-407c-b2f8-95bf5b366187'
    distroAccessOpenAUuid = '1fd3e838-f92a-4086-8308-de17f6fa9d73'
    distroAccessSharedAUuid = '985366e7-7504-4f67-a8ee-90c340ff977a'
    distroAccessClosedAUuid = 'a8adc972-a2b6-4f5b-837b-20f83a685ed6'
    distroLicensesQUuid = '3d89e23d-ff5c-45da-97a8-169ad8c39be6'
    distroLicensesWhatQUuid = 'ca0f9465-3116-4824-8651-b592151c5368'
    distroLicensesWhatCC0AUuid = 'd27a6e0f-55ea-4b25-bfb9-dcb4d6346fe0'
    distroLicensesWhatCCBYAUuid = '9186e183-e328-41f9-b012-149d0bbad9ea'
    distroLicensesWhatOtherAUuid = '734d5f4e-91c0-4019-8164-8c70c2e0c8f2'
    distroLicensesWhatOtherLinkQUuid = '375792f1-d7c3-4c8d-bf9e-f15ffa38e2fb'
    distroLicensesStartQUuid = '28d494ef-26c0-4632-956e-5cafcc498a32'


CONTRIBUTOR_ROLES = {
    UUIDs.contributorRoleContactPersonAUuid: 'contact person',
    UUIDs.contributorRoleDataCollectorAUuid: 'data collector',
    UUIDs.contributorRoleDataCuratorAUuid: 'data curator',
    UUIDs.contributorRoleDataManagerAUuid: 'data manager',
    UUIDs.contributorRoleDataProtectorAUuid: 'data protection officer',
    UUIDs.contributorRoleDataStewardAUuid: 'data steward',
    UUIDs.contributorRoleDistributorAUuid: 'distributor',
    UUIDs.contributorRoleEditorAUuid: 'editor',
    UUIDs.contributorRoleProducerAUuid: 'producer',
    UUIDs.contributorRoleProjectLeaderAUuid: 'project leader',
    UUIDs.contributorRoleProjectManagerAUuid: 'project manager',
    UUIDs.contributorRoleProjectMemberAUuid: 'project member',
    UUIDs.contributorRoleResearcherAUuid: 'researcher',
    UUIDs.contributorRoleRightsHolderAUuid: 'rights holder',
    UUIDs.contributorRoleSponsorAUuid: 'sponsor',
    UUIDs.contributorRoleSupervisorAUuid: 'supervisor',
    UUIDs.contributorRoleWorkPackageLeaderAUuid: 'work package leader',
    UUIDs.contributorRoleWorkCreatorOfDMPAUuid: 'creator of DMP',
    UUIDs.contributorRoleOtherAUuid: 'other',
}

FUNDING_STATUSES = {
    UUIDs.projectFundingStatusPlannedAUuid: 'planned',
    UUIDs.projectFundingStatusAppliedAUuid: 'applied',
    UUIDs.projectFundingStatusGrantedAUuid: 'granted',
    UUIDs.projectFundingStatusRejectedAUuid: 'rejected',
}

YES_NO = {
    UUIDs.producingPersonalYesAUuid: 'yes',
    UUIDs.producingPersonalNoAUuid: 'no',
    UUIDs.producingSensitiveYesAUuid: 'yes',
    UUIDs.producingSensitiveNoAUuid: 'no',
}

DATASET_TYPES = {
    UUIDs.producingTypeRawAUuid: 'raw data',
    UUIDs.producingTypeIntermediateAUuid: 'intermediate data',
    UUIDs.producingTypeProcessedUnpublishableAUuid: 'processed data',
    UUIDs.producingTypeProcessedPublishedAUuid: 'processed data',
}

DATASET_ID_TYPES = {
    UUIDs.producingIdsTypeHandleAUuid: 'handle',
    UUIDs.producingIdsTypeDoiAUuid: 'doi',
    UUIDs.producingIdsTypeArkAUuid: 'ark',
    UUIDs.producingIdsTypeUrlAUuid: 'url',
    UUIDs.producingIdsTypeOtherAUuid: 'other',
}

DATA_ACCESS = {
    UUIDs.distroAccessOpenAUuid: 'open',
    UUIDs.distroAccessSharedAUuid: 'shared',
    UUIDs.distroAccessClosedAUuid: 'closed',
}

LICENSES = {
    UUIDs.distroLicensesWhatCC0AUuid: 'https://creativecommons.org/publicdomain/zero/1.0/',
    UUIDs.distroLicensesWhatCCBYAUuid: 'https://creativecommons.org/licenses/by/4.0/',
}

REPOSITORY_KINDS = {
    UUIDs.distroRepositoryDomainAUuid: 'a domain-specific repository',
    UUIDs.distroRepositoryNationalAUuid: 'a national repository',
    UUIDs.distroRepositoryInstitutionalAUuid: 'an institutional repository',
    UUIDs.distroRepositorySpecialAUuid: 'a special-purpose repository for the project',
    UUIDs.distroRepositoryGeneralAUuid: 'a general-purpose repository',
}

REPOSITORY_WHICH = {
    UUIDs.distroRepositoryDomainAUuid: UUIDs.distroRepositoryDomainWhichQUuid,
    UUIDs.distroRepositoryGeneralAUuid: UUIDs.distroRepositoryGeneralWhichQUuid,
}

COST_ALLOCATIONS = (
    (UUIDs.costAllocationFindabilityAUuid, 'ensuring findability'),
    (UUIDs.costAllocationAccessibilityAUuid, 'ensuring accessibility'),
    (UUIDs.costAllocationInteroperabilityAUuid, 'ensuring interoperability'),
    (UUIDs.costAllocationReusabilityAUuid, 'ensuring reusability'),
    (UUIDs.costManagementAUuid, 'supporting management'),
)

ORCID_RE = re.compile(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]')
URL_RE = re.compile(r'https?://[^\s)\]]+')
CURRENCY_RE = re.compile(r'\b[A-Z]{3}\b')


def _path(*parts: str) -> str:
    return '.'.join(parts)


def markdown_plain(text: str) -> str:
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'^\s{0,3}(#{1,6}|>)\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*([-*+]|\d+\.)\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'(\*\*|__)(.+?)\1', r'\2', text)
    text = re.sub(r'(?<!\w)([*_])(.+?)\1(?!\w)', r'\2', text)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    return ' '.join(text.split())


def _join_sentence(items: list[str]) -> str:
    *init, last = items
    if len(init) > 1:
        return ', '.join(init) + ', and ' + last
    return ' and '.join(items)


class Replies:

    def __init__(self, replies: dict) -> None:
        self.replies = replies

    def _value(self, path: str, reply_type: str) -> Any:
        reply = self.replies.get(path)
        if not isinstance(reply, dict):
            return None
        value = reply.get('value')
        if not isinstance(value, dict) or value.get('type') != reply_type:
            return None
        return value.get('value')

    def answer(self, *path: str) -> str | None:
        return self._value(_path(*path), 'AnswerReply')

    def string(self, *path: str) -> str:
        value = self._value(_path(*path), 'StringReply')
        return value.strip() if isinstance(value, str) else ''

    def text(self, *path: str) -> str:
        return markdown_plain(self.string(*path))

    def items(self, *path: str) -> list[str]:
        return self._value(_path(*path), 'ItemListReply') or []

    def choices(self, *path: str) -> list[str]:
        return self._value(_path(*path), 'MultiChoiceReply') or []

    def integration(self, *path: str) -> dict | None:
        value = self._value(_path(*path), 'IntegrationReply')
        return value if isinstance(value, dict) else None

    def timestamps(self) -> list[str]:
        return sorted(
            reply['createdAt']
            for reply in self.replies.values()
            if isinstance(reply, dict) and isinstance(reply.get('createdAt'), str)
        )


def _integration_raw(reply: dict | None) -> dict:
    if reply and reply.get('type') == 'IntegrationType' and isinstance(reply.get('raw'), dict):
        return reply['raw']
    return {}


def _integration_text(reply: dict | None) -> str:
    return markdown_plain(reply.get('value', '')) if reply else ''


def _orcid(reply: dict | None) -> str | None:
    orcid = _integration_raw(reply).get('orcid-id')
    if isinstance(orcid, str) and ORCID_RE.fullmatch(orcid):
        return orcid
    match = ORCID_RE.search(reply.get('value', '')) if reply else None
    return match.group(0) if match else None


def _funder_id(reply: dict | None) -> dict | None:
    uri = _integration_raw(reply).get('uri')
    if not isinstance(uri, str) or not uri:
        match = URL_RE.search(reply.get('value', '')) if reply else None
        uri = match.group(0) if match else None
    if uri:
        return {'identifier': uri, 'type': 'fundref' if '10.13039/' in uri else 'url'}
    name = _integration_text(reply)
    return {'identifier': name, 'type': 'other'} if name else None


def _currency_code(reply: dict | None) -> str | None:
    code = _integration_raw(reply).get('code')
    if isinstance(code, str) and CURRENCY_RE.fullmatch(code):
        return code
    match = CURRENCY_RE.search(reply.get('value', '')) if reply else None
    return match.group(0) if match else None


def _cost_value(value: str) -> float | int | None:
    value = re.sub(r'\s', '', value)
    if re.fullmatch(r'\d{1,3}(,\d{3})+(\.\d+)?', value):
        value = value.replace(',', '')
    elif re.fullmatch(r'\d+,\d+', value):
        value = value.replace(',', '.')
    try:
        number = float(value)
    except ValueError:
        return None
    return int(number) if number.is_integer() else number


def _contributors(replies: Replies) -> tuple[list[dict], dict | None]:
    path = _path(UUIDs.adminDetailsCUuid, UUIDs.contributorsQUuid)
    contributors = []
    contact = None
    for item in replies.items(path):
        name = replies.string(path, item, UUIDs.contributorNameQUuid)
        email = replies.string(path, item, UUIDs.contributorEmailQUuid)
        orcid = _orcid(replies.integration(path, item, UUIDs.contributorOrcidQUuid))
        role_uuids = replies.choices(path, item, UUIDs.contributorRoleQUuid)
        roles = sorted({CONTRIBUTOR_ROLES.get(role, 'other') for role in role_uuids})
        if not name or not roles:
            continue
        contributor: dict[str, Any] = {
            'contributor_id': {
                'identifier': f'https://orcid.org/{orcid}' if orcid else item,
                'type': 'orcid' if orcid else 'other',
            },
            'name': name,
            'role': roles,
        }
        if email:
            contributor['mbox'] = email
        contributors.append(contributor)
        if contact is None and email and UUIDs.contributorRoleContactPersonAUuid in role_uuids:
            contact = {
                'contact_id': contributor['contributor_id'],
                'mbox': email,
                'name': name,
            }
    if contact is None:
        # Fall back to the first contributor with e-mail if no contact person is specified
        contact = next((
            {'contact_id': c['contributor_id'], 'mbox': c['mbox'], 'name': c['name']}
            for c in contributors if 'mbox' in c
        ), None)
    return contributors, contact


def _fundings(replies: Replies, path: str) -> list[dict]:
    fundings = []
    for item in replies.items(path):
        funder_id = _funder_id(replies.integration(path, item, UUIDs.projectFundingFunderQUuid))
        if funder_id is None:
            continue
        funding: dict[str, Any] = {'funder_id': funder_id}
        status = FUNDING_STATUSES.get(replies.answer(path, item, UUIDs.projectFundingStatusQUuid) or '')
        if status:
            funding['funding_status'] = status
        grant_number = replies.string(path, item, UUIDs.projectFundingGrantNumberQUuid)
        if grant_number:
            funding['grant_id'] = {'identifier': grant_number, 'type': 'other'}
        fundings.append(funding)
    return fundings


def _projects(replies: Replies) -> list[dict]:
    path = _path(UUIDs.adminDetailsCUuid, UUIDs.projectsQUuid)
    projects = []
    for item in replies.items(path):
        name = replies.string(path, item, UUIDs.projectNameQUuid)
        if not name:
            continue
        project: dict[str, Any] = {'title': name}
        description = replies.text(path, item, UUIDs.projectAbstractQUuid)
        if description:
            project['description'] = description
        for key, question in (('start', UUIDs.projectStartQUuid), ('end', UUIDs.projectEndQUuid)):
            value = replies.string(path, item, question)
            if value:
                project[key] = value
        fundings = _fundings(replies, _path(path, item, UUIDs.projectFundingQUuid))
        if fundings:
            project['funding'] = fundings
        projects.append(project)
    return projects


def _cost_description(replies: Replies, path: str) -> str:
    choices = replies.choices(path, UUIDs.costAllocationQUuid)
    allocations = [label for uuid, label in COST_ALLOCATIONS if uuid in choices]
    parts = []
    description = replies.text(path, UUIDs.costDescriptionQUuid)
    if description:
        parts.append(description if description.endswith('.') else f'{description}.')
    if allocations:
        parts.append(f'This resource is allocated for {_join_sentence(allocations)} of data.')
    return ' '.join(parts)


def _costs(replies: Replies) -> list[dict]:
    projects_path = _path(UUIDs.adminDetailsCUuid, UUIDs.projectsQUuid)
    costs = []
    for project_item in replies.items(projects_path):
        costs_path = _path(projects_path, project_item, UUIDs.costQUuid)
        for item in replies.items(costs_path):
            path = _path(costs_path, item)
            title = replies.string(path, UUIDs.costTitleQUuid)
            if not title:
                continue
            cost: dict[str, Any] = {'title': title}
            description = _cost_description(replies, path)
            if description:
                cost['description'] = description
            value = _cost_value(replies.string(path, UUIDs.costAmountQUuid))
            if value is not None:
                cost['value'] = value
            currency = _currency_code(replies.integration(path, UUIDs.costCurrencyQUuid))
            if currency:
                cost['currency_code'] = currency
            costs.append(cost)
    return costs


def _preservation_statement(replies: Replies, path: str) -> str:
    sentences = []
    kept = replies.answer(path, UUIDs.keptQUuid)
    if kept == UUIDs.keptTechnicallyPossibleAUuid:
        sentences.append('The data set will be kept as long as technically possible.')
    elif kept == UUIDs.keptUntilDeletedAUuid:
        sentences.append('The data set will be kept until it needs to be deleted for legal, contractual or regulatory reasons.')
    elif kept == UUIDs.keptFixedPeriodAUuid:
        period = replies.string(path, UUIDs.keptQUuid, UUIDs.keptFixedPeriodAUuid, UUIDs.keptFixedPeriodHowLongQUuid)
        sentences.append(f'The data set will be kept for a fixed period ({period}).' if period else 'The data set will be kept for a fixed period.')
    metadata = replies.answer(path, UUIDs.keptMetadataQUuid)
    if metadata == UUIDs.keptMetadataYesAUuid:
        sentences.append('The metadata will be available even when the data no longer exists.')
    elif metadata == UUIDs.keptMetadataNoAUuid:
        sentences.append('The metadata will not be available when the data no longer exists.')
    return ' '.join(sentences)


def _licenses(replies: Replies, path: str) -> list[dict]:
    licenses = []
    for item in replies.items(path):
        what = replies.answer(path, item, UUIDs.distroLicensesWhatQUuid)
        if what == UUIDs.distroLicensesWhatOtherAUuid:
            license_ref = replies.string(path, item, UUIDs.distroLicensesWhatQUuid, what, UUIDs.distroLicensesWhatOtherLinkQUuid)
        else:
            license_ref = LICENSES.get(what or '', '')
        start_date = replies.string(path, item, UUIDs.distroLicensesStartQUuid)
        if license_ref and start_date:
            licenses.append({'license_ref': license_ref, 'start_date': start_date})
    return licenses


def _host(replies: Replies, path: str) -> tuple[str, dict | None]:
    kind = replies.answer(path, UUIDs.distroRepositoryQUuid) or ''
    description = REPOSITORY_KINDS.get(kind, '')
    which = REPOSITORY_WHICH.get(kind)
    reply = replies.integration(path, UUIDs.distroRepositoryQUuid, kind, which) if which else None
    raw = _integration_raw(reply)
    name = raw.get('name') if isinstance(raw.get('name'), str) else _integration_text(reply)
    if not name:
        return description, None
    description = f'{description} ({name})' if description else name
    url = raw.get('homepage') or (f'https://fairsharing.org/{raw["id"]}' if raw.get('id') else None)
    return description, {'title': name, 'url': url} if url else None


def _distributions(replies: Replies, path: str, title: str) -> list[dict]:
    if replies.answer(path, UUIDs.publishedQUuid) != UUIDs.publishedYesAUuid:
        return []
    distros_path = _path(path, UUIDs.publishedQUuid, UUIDs.publishedYesAUuid, UUIDs.distrosQUuid)
    distributions = []
    for item in replies.items(distros_path):
        data_access = DATA_ACCESS.get(replies.answer(distros_path, item, UUIDs.distroAccessQUuid) or '')
        if not data_access:
            continue
        distribution: dict[str, Any] = {'title': title, 'data_access': data_access}
        repository, host = _host(replies, _path(distros_path, item))
        if repository:
            distribution['description'] = f'Distributed via {repository}.'
        if host:
            distribution['host'] = host
        licenses = _licenses(replies, _path(distros_path, item, UUIDs.distroLicensesQUuid))
        if licenses:
            distribution['license'] = licenses
        distributions.append(distribution)
    return distributions


def _dataset_id(replies: Replies, path: str, item: str) -> dict:
    ids_path = _path(path, UUIDs.producingIdsQUuid)
    for id_item in replies.items(ids_path):
        id_type = replies.answer(ids_path, id_item, UUIDs.producingIdsTypeQUuid) or ''
        identifier = replies.string(ids_path, id_item, UUIDs.producingIdsIdQUuid)
        if identifier and id_type != UUIDs.producingIdsTypeNoneAUuid:
            return {'identifier': identifier, 'type': DATASET_ID_TYPES.get(id_type, 'other')}
    return {'identifier': item, 'type': 'other'}


def _datasets(replies: Replies) -> list[dict]:
    datasets_path = _path(UUIDs.preservingCUuid, UUIDs.producingQUuid)
    datasets = []
    for item in replies.items(datasets_path):
        path = _path(datasets_path, item)
        title = replies.string(path, UUIDs.producingNameQUuid) or '(unnamed dataset)'
        dataset: dict[str, Any] = {
            'dataset_id': _dataset_id(replies, path, item),
            'title': title,
            'personal_data': YES_NO.get(replies.answer(path, UUIDs.producingPersonalQUuid) or '', 'unknown'),
            'sensitive_data': YES_NO.get(replies.answer(path, UUIDs.producingSensitiveQUuid) or '', 'unknown'),
        }
        description = replies.text(path, UUIDs.producingDescriptionQUuid)
        if description:
            dataset['description'] = description
        dataset_type = DATASET_TYPES.get(replies.answer(path, UUIDs.producingTypeQUuid) or '')
        if dataset_type:
            dataset['type'] = dataset_type
        preservation_statement = _preservation_statement(replies, path)
        if preservation_statement:
            dataset['preservation_statement'] = preservation_statement
        distributions = _distributions(replies, path, title)
        if distributions:
            dataset['distribution'] = distributions
        datasets.append(dataset)
    return datasets


class _EthicalIssues:

    def __init__(self, replies: Replies) -> None:
        self.replies = replies
        self.answered = False
        self.issues: list[str] = []
        self.descriptions: list[str] = []

    def add(self, description: str, issue: str | None = None) -> None:
        self.descriptions.append(description)
        if issue:
            self.issues.append(issue)

    def answer(self, *path: str) -> str | None:
        answer = self.replies.answer(*path)
        self.answered = self.answered or answer is not None
        return answer

    def exist(self) -> str:
        if self.issues:
            return 'yes'
        return 'no' if self.answered else 'unknown'

    def description(self) -> str:
        return ' '.join(self.descriptions)


NREF_LEGAL_BASES = {
    UUIDs.nrefDataPersonalLegalBasisLegReqAUuid: 'legal requirements',
    UUIDs.nrefDataPersonalLegalBasisVitInterAUuid: 'vital interests',
    UUIDs.nrefDataPersonalLegalBasisLegInterAUuid: 'legitimate interests',
    UUIDs.nrefDataPersonalLegalBasisContractAUuid: 'contract obligations',
}

NREF_ETHICAL_APPROVALS = {
    UUIDs.nrefDataEthicalAppCoversAUuid: 'has been ethically approved and no new approval is needed, as the existing ethical approval under research ethics laws covers our intended reuse of the data.',
    UUIDs.nrefDataEthicalAppExtensionAUuid: 'has been ethically approved and an extension of the existing ethical approval under research ethics laws will be needed for the intended reuse of the data.',
    UUIDs.nrefDataEthicalAppNewAUuid: 'has been ethically approved but new ethical approval under research ethics laws will be required to cover our intended use of the data.',
}

CPERS_CONSENTS = {
    UUIDs.cpersConsentUseAUuid: 'We will collect consent for our specific use of the data.',
    UUIDs.cpersConsentReuseAUuid: 'We will collect consent for our use as well as reuse of the data.',
    UUIDs.cpersConsentUseAnonAUuid: 'We will collect consent for our use of the data and for anonymization; we will anonymize the data afterwards for reuse.',
    UUIDs.cpersConsentAnonAUuid: 'We ask for consent for anonymization; we will anonymise first and all further processing is on the anonymous data.',
}

CPERS_REUSERS = {
    UUIDs.cpersReusersNoAUuid: 'The consent form will not be available for re-users.',
    UUIDs.cpersReusersYesAUuid: 'The consent form will be available for re-users.',
}

CPERS_OTHER_LEGAL_BASES = {
    UUIDs.cpersLegalBasisContractAUuid: 'We require the processing to fulfil our contract with the data subjects.',
    UUIDs.cpersLegalBasisLegitAUuid: 'We have a legitimate interest: data subjects all expect us to do this data processing because of who we are.',
    UUIDs.cpersLegalBasisVitalAUuid: 'We need to do this to save the data subject (i.e. vital interest).',
    UUIDs.cpersLegalBasisLegalAUuid: 'We are legally obliged to do this data processing (i.e. legal requirement).',
}

PRIVACY_ANSWERS = {
    UUIDs.privacyRestrictionsNoAUuid: 'There are no restrictions where the data can be stored.',
    UUIDs.privacyRestrictionsYesEUAUuid: 'Our data must stay in EU.',
    UUIDs.privacyRestrictionsYesCountryAUuid: 'Our data must stay in the same country.',
    UUIDs.privacyRestrictionsYesInstituteAUuid: 'Our data must stay in the same institute.',
    UUIDs.privacyPseudoNoAUuid: 'We cannot make the data more openly available by pseudonymization.',
    UUIDs.privacyPseudoYesAUuid: 'We can make the data more openly available by pseudonymization.',
    UUIDs.privacyAnonNoAUuid: 'We cannot make the data more openly available by anonymization.',
    UUIDs.privacyAnonYesAUuid: 'We can make the data more openly available by anonymization.',
    UUIDs.privacyAggregationNoAUuid: 'We cannot make the data more openly available through data aggregation.',
    UUIDs.privacyAggregationYesAUuid: 'We can make the data more openly available through data aggregation.',
}


def _ethics_reused_data(ethics: _EthicalIssues) -> None:
    replies = ethics.replies
    preexisting_path = _path(UUIDs.reusingCUuid, UUIDs.preexistingQUuid)
    if ethics.answer(preexisting_path) != UUIDs.preexistingYesAUuid:
        return
    path = _path(preexisting_path, UUIDs.preexistingYesAUuid, UUIDs.nrefDataQUuid)
    for item in replies.items(path):
        name = replies.string(path, item, UUIDs.nrefDataNameQUuid) or '(unknown name)'
        where = replies.string(path, item, UUIDs.nrefDataWhereQUuid)
        prefix = f'Non-reference dataset "{name}"' + (f' ({where})' if where else '')
        if replies.answer(path, item, UUIDs.nrefDataUseQUuid) != UUIDs.nrefDataUseYesAUuid:
            continue
        used_path = _path(path, item, UUIDs.nrefDataUseQUuid, UUIDs.nrefDataUseYesAUuid)
        personal = replies.answer(used_path, UUIDs.nrefDataPersonalQUuid)
        if personal == UUIDs.nrefDataPersonalNoAUuid:
            ethics.add(f'{prefix} does not contain any personal data.')
        elif personal == UUIDs.nrefDataPersonalYesAUuid:
            legal_path = _path(used_path, UUIDs.nrefDataPersonalQUuid, personal, UUIDs.nrefDataPersonalLegalBasisQUuid)
            legal_basis = replies.answer(legal_path)
            if legal_basis == UUIDs.nrefDataPersonalLegalBasisPublicInAUuid:
                ethics.add(f'{prefix} contains personal data based on public interest.', 'nref-personal-data')
            elif legal_basis == UUIDs.nrefDataPersonalLegalBasisConsentAUuid:
                reuse = replies.answer(legal_path, legal_basis, UUIDs.nrefDataPersonalConsentReuseQUuid)
                if reuse == UUIDs.nrefDataPersonalConsentReuseNoAUuid:
                    ethics.add(f'{prefix} contains personal data based on consent, but the consent does not cover our intended reuse; new consent is required.', 'nref-personal-data')
                else:
                    ethics.add(f'{prefix} contains personal data based on consent which covers our reuse.', 'nref-personal-data')
            elif legal_basis == UUIDs.nrefDataPersonalLegalBasisOtherAUuid:
                other = NREF_LEGAL_BASES.get(replies.answer(legal_path, legal_basis, UUIDs.nrefDataPersonalLegalBasisOtherQUuid) or '', 'other legal basis')
                ethics.add(f'{prefix} contains personal data based on {other}.', 'nref-personal-data')
            else:
                ethics.add(f'{prefix} contains personal data.', 'nref-personal-data')
        approval = NREF_ETHICAL_APPROVALS.get(replies.answer(used_path, UUIDs.nrefDataEthicalAppQUuid) or '')
        if approval:
            ethics.add(f'{prefix} {approval}', 'nref-ethical-approval')


def _ethics_legal_basis(ethics: _EthicalIssues, gdpr_path: str) -> None:
    replies = ethics.replies
    legal_path = _path(gdpr_path, UUIDs.cpersLegalBasisQUuid)
    legal_basis = replies.answer(legal_path)
    if legal_basis == UUIDs.cpersLegalBasisAskAUuid:
        ethics.add('We ask the data subjects for their consent.')
        consent = CPERS_CONSENTS.get(replies.answer(legal_path, legal_basis, UUIDs.cpersConsentQUuid) or '')
        if consent:
            ethics.add(consent)
        reusers = CPERS_REUSERS.get(replies.answer(legal_path, legal_basis, UUIDs.cpersReusersQUuid) or '')
        if reusers:
            ethics.add(reusers)
    elif legal_basis == UUIDs.cpersLegalBasisPublicAUuid:
        ethics.add('We do this for the benefit of society, and this is more important than the privacy of the subjects (i.e. public interest).')
    elif legal_basis == UUIDs.cpersLegalBasisOtherAUuid:
        other = CPERS_OTHER_LEGAL_BASES.get(replies.answer(legal_path, legal_basis, UUIDs.cpersLegalBasisOtherQUuid) or '')
        if other:
            ethics.add(other)


def _ethics_collected_data(ethics: _EthicalIssues) -> None:
    replies = ethics.replies
    collect_path = _path(UUIDs.creatingCUuid, UUIDs.collectPersonalQUuid)
    if ethics.answer(collect_path) == UUIDs.collectPersonalYesAUuid:
        ethics.add('We will collect data connected to a person, i.e. "personal data".', 'collect-personal-data')
        gdpr_path = _path(collect_path, UUIDs.collectPersonalYesAUuid, UUIDs.cpersGdprQUuid)
        if replies.answer(gdpr_path) == UUIDs.cpersGdprExploreAUuid:
            gdpr_path = _path(gdpr_path, UUIDs.cpersGdprExploreAUuid)
            _ethics_legal_basis(ethics, gdpr_path)
            if replies.answer(gdpr_path, UUIDs.cpersNeedDpiaQUuid) == UUIDs.cpersNeedDpiaYesAUuid:
                ethics.add('We need to conduct a data protection impact assessment (DPIA).', 'dpia')

    legislation_path = _path(UUIDs.creatingCUuid, UUIDs.ethicsLegislationQUuid)
    if ethics.answer(legislation_path) == UUIDs.ethicsLegislationYesAUuid:
        ethics.add('The data collection is subject to ethical legislation.', 'ethical-legislation')
        yes_path = _path(legislation_path, UUIDs.ethicsLegislationYesAUuid)
        review = replies.answer(yes_path, UUIDs.ethicsReviewQUuid)
        if review == UUIDs.ethicsReviewYesAUuid:
            ethics.add('The data collection is covered by an ethical review.')
        elif review == UUIDs.ethicsReviewNoAUuid:
            ethics.add('The data collection is not covered by an ethical review.')
        if replies.answer(yes_path, UUIDs.ethicsHumanSubjectsQUuid) == UUIDs.ethicsHumanSubjectsYesAUuid:
            ethics.add('The data collection involves human subjects.', 'human-subjects')


def _ethics_access(ethics: _EthicalIssues) -> None:
    replies = ethics.replies
    can_open_path = _path(UUIDs.givingAccessCUuid, UUIDs.canOpenQUuid)
    if ethics.answer(can_open_path) != UUIDs.canOpenNoAUuid:
        return
    legal_path = _path(can_open_path, UUIDs.canOpenNoAUuid, UUIDs.legalReasonsQUuid)
    if replies.answer(legal_path) != UUIDs.legalReasonsYesAUuid:
        return
    ethics.add('There are legal reasons why some of our data cannot be open.', 'legal-reasons')
    privacy_path = _path(legal_path, UUIDs.legalReasonsYesAUuid, UUIDs.privacyReasonsQUuid)
    if replies.answer(privacy_path) != UUIDs.privacyReasonsYesAUuid:
        return
    ethics.add('There are privacy reasons why some of our data cannot be open.', 'privacy-reasons')
    for question in (UUIDs.privacyRestrictionsQUuid, UUIDs.privacyPseudoQUuid, UUIDs.privacyAnonQUuid, UUIDs.privacyAggregationQUuid):
        sentence = PRIVACY_ANSWERS.get(replies.answer(privacy_path, UUIDs.privacyReasonsYesAUuid, question) or '')
        if sentence:
            ethics.add(sentence)


def _ethical_issues(replies: Replies) -> tuple[str, str]:
    ethics = _EthicalIssues(replies)
    _ethics_reused_data(ethics)
    _ethics_collected_data(ethics)
    _ethics_access(ethics)
    return ethics.exist(), ethics.description()


def check_knowledge_model(project_data: dict) -> str:
    package = project_data.get('knowledgeModelPackage') or {}
    package_id = ':'.join(package.get(key, '') for key in ('organizationId', 'kmId', 'version'))
    if not package_id.startswith(SUPPORTED_KM_PREFIXES):
        msg = f'Unsupported knowledge model package: {package_id}'
        raise ValueError(msg)
    return package_id


def to_madmp(project_data: dict, client_url: str, created: str, modified: str) -> dict:
    package_id = check_knowledge_model(project_data)
    package_name = (project_data.get('knowledgeModelPackage') or {}).get('name', package_id)
    replies = Replies(project_data.get('replies') or {})
    project_uuid = project_data.get('uuid')

    contributors, contact = _contributors(replies)
    ethical_issues_exist, ethical_issues_description = _ethical_issues(replies)

    dmp: dict[str, Any] = {
        'title': project_data.get('name'),
        'description': (f'This maDMP has been exported from {client_url} and is based on knowledge model '
                        f'{package_name} ({package_id}). The project is identified by UUID "{project_uuid}" '
                        f'within this instance.'),
        'language': 'eng',
        'created': created,
        'modified': modified,
        'dmp_id': {
            'identifier': f'{client_url}/projects/{project_uuid}',
            'type': 'url',
        },
        'ethical_issues_exist': ethical_issues_exist,
        'dataset': _datasets(replies),
    }
    if contact:
        dmp['contact'] = contact
    if contributors:
        dmp['contributor'] = contributors
    if ethical_issues_description:
        dmp['ethical_issues_description'] = ethical_issues_description
    projects = _projects(replies)
    if projects:
        dmp['project'] = projects
    costs = _costs(replies)
    if costs:
        dmp['cost'] = costs
    return {'dmp': dmp}
