import re
import typing

import httpx


class WizardClient:

    def __init__(self, api_url: str, client: httpx.AsyncClient) -> None:
        self.api_url = api_url.rstrip('/')
        self.client = client
        self.client.base_url = httpx.URL(self.api_url)
        self.client.headers.update({
            'User-Agent': 'maDMP-Wizard-Client/0.1.0',
        })

    @property
    def client_url(self) -> str:
        return self.api_url[:-4]

    async def get_project(self, project_uuid: str, user_token: str) -> dict:
        response = await self.client.get(
            url=f'/projects/{project_uuid}/questionnaire',
            headers={
                'Authorization': f'Bearer {user_token}',
            },
        )
        response.raise_for_status()
        return response.json()

    def to_madmp(self, project_data: dict) -> dict:
        package_id = project_data.get('knowledgeModelPackageId', '::')
        if not package_id.startswith('dsw:root:'):
            msg = f'Unsupported knowledge model package: {package_id}'
            raise ValueError(msg)
        dmp = map_dsw_root_to_madmp(self.client_url, project_data)
        return {'dmp': dmp}


# Old mapping to be reworked with KM annotations
class UUIDs:
    adminDetailsCUuid = '1e85da40-bbfc-4180-903e-6c569ed2da38'
    contributorsQUuid = '73d686bd-7939-412e-8631-502ee6d9ea7b'
    contributorNameQUuid = '6155ad47-3d1e-4488-9f2a-742de1e56580'
    contributorEmailQUuid = '3a2ffc13-6a0e-4976-bb34-14ab6d938348'
    contributorOrcidQUuid = '6295a55d-48d7-4f3c-961a-45b38eeea41f'
    contributorAffiliationQUuid = '68530470-1f1c-4448-8593-63a288713a66'
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
    nrefDataEthicalAppNotApplicableAUuid = 'ad44fec7-d244-4bb1-9028-8d6856a06d6b'
    nrefDataEthicalAppCoversAUuid = '284110a8-66b4-4ba5-9e7a-edb77b1f2b3a'
    nrefDataEthicalAppExtensionAUuid = '12ae8bdc-a6eb-4db9-9a1a-7e6fed7f9ace'
    nrefDataEthicalAppNewAUuid = '6dd1142d-f76f-4d0b-9c38-999f7d8a229b'
    creatingCUuid = 'b1df3c74-0b1f-4574-81c4-4cc2d780c1af'
    collectPersonalQUuid = '49c009cb-a38c-4836-9780-8a8b3dd1cbac'
    collectPersonalNoAUuid = '4bdc319d-282a-4a80-9cdd-78d2081e812b'
    collectPersonalYesAUuid = '421e2d3e-c95c-4244-9465-de8f1cb8aeba'
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
    cpersLegalBasisContractAUuid = '1dfe0a6d-4281-4d5e-bcaa-5e20fa28a591'
    cpersLegalBasisLegitAUuid = '9d5e3104-2b6b-4d95-848e-253ef069d8b3'
    cpersLegalBasisVitalAUuid = '557a5401-a94a-4a37-af2e-a21829557bfa'
    cpersLegalBasisLegalAUuid = 'f10de3a8-2751-42c7-afaa-92eed4833f8e'
    cpersLegalBasisPublicAUuid = 'c732f0b9-2f66-47f4-902f-724a44cdfd4b'
    cpersEthicReviewQUuid = 'ebcbf4c6-ce25-4a0b-9e82-039a88498203'
    cpersEthicReviewYesAUuid = '9310b639-4cf7-4f94-8fbe-c1afc50afe4b'
    cpersEthicReviewNoAUuid = '579c0a9a-29f0-4ab8-991d-bc4f55f2e4b8'
    cpersNeedDpiaQUuid = '8915bd25-db22-4ed6-bcc8-b1bbdc52989e'
    cpersNeedDpiaYesAUuid = 'c3914e43-cca1-4180-8960-228b7022bae6'
    cpersNeedDpiaNoAUuid = 'd0741ff3-370b-44e7-860d-00b1f01e6254'
    givingAccessCUuid = '6be88f7c-f868-460f-bba7-91e1c659adfd'
    canOpenQUuid = 'a549d10b-aa46-4c0c-863f-30219ac5ecce'
    canOpenNoAUuid = 'b3739ebd-2d8e-42d3-9425-a7d6d1b26c79'
    canOpenYesAUuid = '8c33553c-9603-4156-82d7-85ab3d7de090'
    legalReasonsQUuid = 'c010e830-bd89-460d-9498-cb41e7ffeb87'
    legalReasonsNoAUuid = '31f2fcda-dbb2-40f6-871b-c3cc59797a6b'
    legalReasonsYesAUuid = 'aac95530-2978-4759-803b-64721533faf0'
    privacyReasonsQUuid = '019db0b3-9067-4134-8bfd-76db3cfc572a'
    privacyReasonsNoAUuid = 'b6dfc087-93d6-4dcf-b45c-3c6600395ec6'
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
    producingIdsQUuid = 'cf727a0a-78c4-45a7-aa9b-cf7650ae873a'
    producingIdsTypeQUuid = '5c22cf59-89e3-43a1-af10-1af43a97bcb2'
    producingIdsTypeHandleAUuid = 'b93a037a-006a-486f-87e0-6bef5c28879b'
    producingIdsTypeDoiAUuid = '48062bc9-0ffb-4509-bec6-e90641a30569'
    producingIdsTypeArkAUuid = 'c353f027-823b-4242-9149-37dca26cf4bc'
    producingIdsTypeUrlAUuid = '7a1d3b28-5f85-48b8-b052-2448c276d9fc'
    producingIdsTypeOtherAUuid = '97236701-7b62-40f8-99a0-3b18d3fe3658'
    producingIdsIdQUuid = '9e13b2d3-5f00-4e19-8a52-5c33c5b1cb07'
    producingPersonalQUuid = 'a1d76760-053c-4706-80a2-cfb6c6a061f3'
    producingPersonalNoAUuid = '4b2a08c7-4942-41fc-8114-d3868c882624'
    producingPersonalYesAUuid = '0cdc4817-7c54-4ec1-b2f4-5c007a85c7b8'
    producingSensitiveQUuid = 'cc95b399-7d8d-4232-bccf-686f78c91bff'
    producingSensitiveNoAUuid = '60de66a3-d303-4784-8931-bc58f8a3e747'
    producingSensitiveYesAUuid = '2686575d-cd74-4e2c-8524-eaca6f510425'
    publishedQUuid = 'a063da1c-aaea-4e18-85ec-f560d833f292'
    publishedYesAUuid = '8d1b07a7-f177-41f5-9532-05536223a8d6'
    distrosQUuid = '81d3095e-a530-40a4-878e-ced42fabc4cd'
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
    UUIDs.contributorRoleSupervisorAUuid: 'supervis<or',
    UUIDs.contributorRoleWorkPackageLeaderAUuid: 'work package leader',
    UUIDs.contributorRoleWorkCreatorOfDMPAUuid: 'creator of DMP',
    UUIDs.contributorRoleOtherAUuid: 'other',
}


def _path(*parts: str) -> str:
    return '.'.join(parts)


def _reply_value_str(reply: typing.Any, default: str | None = None) -> str | None:
    if not isinstance(reply, dict):
        return default
    result = reply.get('value', {}).get('value', default)
    if result is not None and not isinstance(result, str):
        return str(result)
    return result


def _reply_value_list(reply: typing.Any, default: list | None = None) -> list | None:
    if not isinstance(reply, dict):
        return default
    result = reply.get('value', {}).get('value', default)
    if result is not None and not isinstance(result, list):
        return [result]
    return result


def _reply_value_dict(reply: typing.Any, default: dict | None = None) -> dict | None:
    if not isinstance(reply, dict):
        return default
    result = reply.get('value', {}).get('value', default)
    if result is not None and not isinstance(result, dict):
        return {'value': result}
    return result


def _reply_orcid(reply: dict) -> str:
    value = _reply_value_dict(reply, {}) or {}
    v = value.get('value', '')
    if value and value.get('type') == 'IntegrationType':
        raw = value.get('raw')
        if raw is not None and isinstance(raw, dict):
            return raw.get('orcid-id', '')
        if v.startswith('ORCID:'):
            orcid = v.split(':', 1)[1].strip().replace('**', '')
            if re.match(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$', orcid):
                return orcid
            return ''
    return v


def _reply_crossref(reply: dict) -> str:
    value = _reply_value_dict(reply, {}) or {}
    v = value.get('value', '')
    if value and value.get('type') == 'IntegrationType':
        raw = value.get('raw')
        if raw is not None and isinstance(raw, dict):
            return raw.get('uri', '')
        return v.rsplit(' ![]', 1)[0].strip().replace('**', '')
    return v


def _reply_currency(reply: dict) -> str:
    value = _reply_value_dict(reply, {}) or {}
    v = value.get('value', '')
    if value and value.get('type') == 'IntegrationType':
        raw = value.get('raw')
        if raw is not None and isinstance(raw, dict):
            return raw.get('code', '')
        return v.rsplit(' ![]', 1)[0].strip().replace('**', '')
    return v


def _get_contributors(replies: dict) -> tuple[list, list]:
    contributors_path = _path(UUIDs.adminDetailsCUuid, UUIDs.contributorsQUuid)
    contributors_items = _reply_value_list(replies.get(contributors_path, {}), []) or []
    contributors, contacts = [], []
    for item in contributors_items:
        name = _reply_value_str(replies.get(_path(contributors_path, item, UUIDs.contributorNameQUuid)))
        email = _reply_value_str(replies.get(_path(contributors_path, item, UUIDs.contributorEmailQUuid)))
        orcid_reply = replies.get(_path(contributors_path, item, UUIDs.contributorOrcidQUuid))
        role_choices = _reply_value_list(replies.get(_path(contributors_path, item, UUIDs.contributorRoleQUuid), [])) or []
        orcid = None
        roles = [CONTRIBUTOR_ROLES[role_uuid] for role_uuid in role_choices if role_uuid in CONTRIBUTOR_ROLES]
        if orcid_reply is None:
            contributor: dict[str, typing.Any] = {
                'contributor_id': {
                    'identifier': item,
                    'type': 'other',
                },
            }
        else:
            orcid = _reply_orcid(orcid_reply)
            contributor: dict[str, typing.Any] = {
                'contributor_id': {
                    'identifier': orcid,
                    'type': 'orcid',
                },
            }
        contributor['name'] = name
        contributor['role'] = roles
        if email:
            contributor['mbox'] = email
        if orcid and name and len(roles) > 0:
            contributors.append(contributor)
            if UUIDs.contributorRoleContactPersonAUuid in role_choices and email:
                contacts.append(contributor)
    return contributors, contacts


def _get_ethical_issues(replies: dict) -> tuple[str, str]:
    issues = []
    descriptions = []

    preexisting_path = _path(UUIDs.reusingCUuid, UUIDs.preexistingQUuid)
    preexisting_answer = replies.get(preexisting_path, '')
    if preexisting_answer == UUIDs.preexistingYesAUuid:
        nref_data_path = _path(preexisting_path, UUIDs.preexistingYesAUuid, UUIDs.nrefDataQUuid)
        nref_data_items = _reply_value_list(replies.get(nref_data_path, {}), []) or []
        for nref_data_item in nref_data_items:
            nref_data_prefix = _path(nref_data_path, nref_data_item)
            nref_data_used_prefix = _path(nref_data_prefix, UUIDs.nrefDataUseQUuid, UUIDs.nrefDataUseYesAUuid)
            name = _reply_value_str(replies.get(_path(nref_data_prefix, UUIDs.nrefDataNameQUuid)), '(unknown dataset)')
            where = _reply_value_str(replies.get(_path(nref_data_prefix, UUIDs.nrefDataWhereQUuid)), 'unknown location')
            personal_answer = replies.get(_path(nref_data_used_prefix, UUIDs.nrefDataPersonalQUuid))
            ethical_app_answer = replies.get(_path(nref_data_used_prefix, UUIDs.nrefDataEthicalAppQUuid))
            if where:
                name = f'"{name}" ({where})'
            prefix = f'Non-reference dataset {name}'
            if personal_answer == UUIDs.nrefDataPersonalNoAUuid:
                descriptions.append(f'{prefix} does not contain personal data.')
            elif personal_answer == UUIDs.nrefDataPersonalYesAUuid:
                legal_basis_path = _path(nref_data_prefix, UUIDs.nrefDataPersonalQUuid, UUIDs.nrefDataPersonalYesAUuid, UUIDs.nrefDataPersonalLegalBasisQUuid)
                legal_basis_answer = replies.get(legal_basis_path, '')
                issues.append('nref-personal-data')
                if legal_basis_answer == UUIDs.nrefDataPersonalLegalBasisPublicInAUuid:
                    descriptions.append(f'{prefix} contains personal data that can be reused based on public interest.')
                elif legal_basis_answer == UUIDs.nrefDataPersonalLegalBasisConsentAUuid:
                    consent_reuse_answer = replies.get(_path(legal_basis_path, UUIDs.nrefDataPersonalLegalBasisConsentAUuid, UUIDs.nrefDataPersonalConsentReuseQUuid), '')
                    if consent_reuse_answer == UUIDs.nrefDataPersonalConsentReuseYesAUuid:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on consent.')
                    elif consent_reuse_answer == UUIDs.nrefDataPersonalConsentReuseNoAUuid:
                        descriptions.append(f'{prefix} contains personal data that cannot be reused based on consent.')
                    else:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on consent, but reuse conditions are unknown.')
                elif legal_basis_answer == UUIDs.nrefDataPersonalLegalBasisOtherAUuid:
                    other_answer = _reply_value_str(replies.get(_path(legal_basis_path, UUIDs.nrefDataPersonalLegalBasisOtherAUuid, UUIDs.nrefDataPersonalLegalBasisOtherQUuid)), '')
                    if other_answer == UUIDs.nrefDataPersonalLegalBasisLegReqAUuid:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on legal requirements.')
                    elif other_answer == UUIDs.nrefDataPersonalLegalBasisVitInterAUuid:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on vital interests.')
                    elif other_answer == UUIDs.nrefDataPersonalLegalBasisLegInterAUuid:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on legitimate interests.')
                    elif other_answer == UUIDs.nrefDataPersonalLegalBasisContractAUuid:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on contract.')
                    else:
                        descriptions.append(f'{prefix} contains personal data that can be reused based on other legal basis.')
                else:
                    descriptions.append(f'{prefix} contains personal data, but legal basis for reuse is unknown.')
            if ethical_app_answer == UUIDs.nrefDataEthicalAppCoversAUuid:
                descriptions.append(f'{prefix} is covered by an ethical approval.')
                issues.append('nref-ethical-approval')
            elif ethical_app_answer == UUIDs.nrefDataEthicalAppExtensionAUuid:
                descriptions.append(f'{prefix} requires an extension of an existing ethical approval.')
                issues.append('nref-ethical-approval-extension')
            elif ethical_app_answer == UUIDs.nrefDataEthicalAppNewAUuid:
                descriptions.append(f'{prefix} requires a new ethical approval.')
                issues.append('nref-ethical-approval-new')

    collect_personal_path = _path(UUIDs.creatingCUuid, UUIDs.collectPersonalQUuid)
    collect_personal_answer = replies.get(collect_personal_path, '')
    if collect_personal_answer == UUIDs.collectPersonalYesAUuid:
        descriptions.append('The project involves collecting personal data.')
        issues.append('collect-personal-data')
        legal_basis_path = _path(collect_personal_path, UUIDs.collectPersonalYesAUuid, UUIDs.cpersLegalBasisQUuid)
        legal_basis_answer = replies.get(legal_basis_path, '')
        if legal_basis_answer == UUIDs.cpersLegalBasisAskAUuid:
            descriptions.append('The legal basis for collecting personal data will be determined after asking the data subjects.')
            consent_path = _path(legal_basis_path, UUIDs.cpersLegalBasisAskAUuid, UUIDs.cpersConsentQUuid)
            consent_answer = replies.get(consent_path, '')
            if consent_answer == UUIDs.cpersConsentUseAUuid:
                descriptions.append('The data subjects will be asked for consent to use their personal data.')
            elif consent_answer == UUIDs.cpersConsentReuseAUuid:
                descriptions.append('The data subjects will be asked for consent to reuse their personal data.')
            elif consent_answer == UUIDs.cpersConsentUseAnonAUuid:
                descriptions.append('We will collect consent for our use of the data and for anonymization; we will anonymize the data afterwards for reuse.')
            elif consent_answer == UUIDs.cpersConsentAnonAUuid:
                descriptions.append('We ask for consent for anonymization; we will anonymise first and all further processing is on the anonymous data.')
            reusers_path = _path(legal_basis_path, UUIDs.cpersLegalBasisAskAUuid, UUIDs.cpersReusersQUuid)
            reusers_answer = replies.get(reusers_path, '')
            if reusers_answer == UUIDs.cpersReusersYesAUuid:
                descriptions.append('The data subjects will be asked for consent to share their personal data with re-users.')
            elif reusers_answer == UUIDs.cpersReusersNoAUuid:
                descriptions.append('The data subjects will not be asked for consent to share their personal data with re-users.')
        elif legal_basis_answer == UUIDs.cpersLegalBasisContractAUuid:
            descriptions.append('The legal basis for collecting personal data is contract.')
        elif legal_basis_answer == UUIDs.cpersLegalBasisLegitAUuid:
            descriptions.append('The legal basis for collecting personal data is legitimate interests.')
        elif legal_basis_answer == UUIDs.cpersLegalBasisVitalAUuid:
            descriptions.append('The legal basis for collecting personal data is vital interests.')
        elif legal_basis_answer == UUIDs.cpersLegalBasisLegalAUuid:
            descriptions.append('The legal basis for collecting personal data is compliance with a legal obligation.')
        elif legal_basis_answer == UUIDs.cpersLegalBasisPublicAUuid:
            descriptions.append('The legal basis for collecting personal data is public interest.')
        else:
            descriptions.append('The legal basis for collecting personal data is unknown.')

        ethic_review_answer = replies.get(_path(collect_personal_path, UUIDs.collectPersonalYesAUuid, UUIDs.cpersEthicReviewQUuid))
        if ethic_review_answer == UUIDs.cpersEthicReviewYesAUuid:
            descriptions.append('The project has undergone ethical review.')
            issues.append('ethical-review')
        elif ethic_review_answer == UUIDs.cpersEthicReviewNoAUuid:
            descriptions.append('The project has not undergone ethical review.')

        need_dpia_answer = replies.get(_path(collect_personal_path, UUIDs.collectPersonalYesAUuid, UUIDs.cpersNeedDpiaQUuid))
        if need_dpia_answer == UUIDs.cpersNeedDpiaYesAUuid:
            descriptions.append('A data protection impact assessment (DPIA) is needed for the collection of personal data.')
            issues.append('dpia-needed')
        elif need_dpia_answer == UUIDs.cpersNeedDpiaNoAUuid:
            descriptions.append('A data protection impact assessment (DPIA) is not needed for the collection of personal data.')

    can_open_path = _path(UUIDs.givingAccessCUuid, UUIDs.canOpenQUuid)
    can_open_answer = replies.get(can_open_path, '')
    if can_open_answer == UUIDs.canOpenNoAUuid:
        legal_reasons_path = _path(can_open_path, UUIDs.canOpenNoAUuid, UUIDs.legalReasonsQUuid)
        legal_reasons_answer = replies.get(legal_reasons_path, '')
        if legal_reasons_answer == UUIDs.legalReasonsYesAUuid:
            descriptions.append('There are legal reasons that prevent the project from giving open access to its data.')
            issues.append('legal-reasons')

            privacy_restrictions_answer = replies.get(_path(legal_reasons_path, UUIDs.legalReasonsYesAUuid, UUIDs.privacyRestrictionsQUuid), '')
            pseudonymization_answer = replies.get(_path(legal_reasons_path, UUIDs.legalReasonsYesAUuid, UUIDs.privacyPseudoQUuid), '')
            anonymization_answer = replies.get(_path(legal_reasons_path, UUIDs.legalReasonsYesAUuid, UUIDs.privacyAnonQUuid), '')
            aggregation_answer = replies.get(_path(legal_reasons_path, UUIDs.legalReasonsYesAUuid, UUIDs.privacyAggregationQUuid), '')

            if privacy_restrictions_answer == UUIDs.privacyRestrictionsNoAUuid:
                descriptions.append('There are no privacy restrictions that prevent the project from giving open access to its data.')
            elif privacy_restrictions_answer == UUIDs.privacyRestrictionsYesEUAUuid:
                descriptions.append('There are privacy restrictions based on the European Union that prevent the project from giving open access to its data.')
            elif privacy_restrictions_answer == UUIDs.privacyRestrictionsYesCountryAUuid:
                descriptions.append('There are privacy restrictions based on the country of the project that prevent it from giving open access to its data.')
            elif privacy_restrictions_answer == UUIDs.privacyRestrictionsYesInstituteAUuid:
                descriptions.append('There are privacy restrictions based on the institute of the project that prevent it from giving open access to its data.')

            if pseudonymization_answer == UUIDs.privacyPseudoNoAUuid:
                descriptions.append('Pseudonymization is not used to prevent the project from giving open access to its data.')
            elif pseudonymization_answer == UUIDs.privacyPseudoYesAUuid:
                descriptions.append('Pseudonymization is used to prevent the project from giving open access to its data.')
                issues.append('pseudonymization')

            if anonymization_answer == UUIDs.privacyAnonNoAUuid:
                descriptions.append('Anonymization is not used to prevent the project from giving open access to its data.')
            elif anonymization_answer == UUIDs.privacyAnonYesAUuid:
                descriptions.append('Anonymization is used to prevent the project from giving open access to its data.')
                issues.append('anonymization')

            if aggregation_answer == UUIDs.privacyAggregationNoAUuid:
                descriptions.append('Aggregation is not used to prevent the project from giving open access to its data.')
            elif aggregation_answer == UUIDs.privacyAggregationYesAUuid:
                descriptions.append('Aggregation is used to prevent the project from giving open access to its data.')
                issues.append('aggregation')

    exist = 'yes' if len(issues) > 0 else 'no'
    description = ' '.join(descriptions).strip()
    return exist, description


def _get_projects(replies: dict) -> list:
    projects_path = _path(UUIDs.adminDetailsCUuid, UUIDs.projectsQUuid)
    projects_items = _reply_value_list(replies.get(projects_path, {}), []) or []
    projects = []
    for item in projects_items:
        name = _reply_value_str(replies.get(_path(projects_path, item, UUIDs.projectNameQUuid)))
        abstract = _reply_value_str(replies.get(_path(projects_path, item, UUIDs.projectAbstractQUuid)))
        start = _reply_value_str(replies.get(_path(projects_path, item, UUIDs.projectStartQUuid)))
        end = _reply_value_str(replies.get(_path(projects_path, item, UUIDs.projectEndQUuid)))

        fundings_path = _path(projects_path, item, UUIDs.projectFundingQUuid)
        funding_items = _reply_value_list(replies.get(fundings_path, {}), []) or []
        fundings = []
        for funding_item in funding_items:
            funder_reply = replies.get(_path(fundings_path, funding_item, UUIDs.projectFundingFunderQUuid), {})
            funder_url = ''
            if funder_reply:
                funder_url = _reply_crossref(funder_reply)
            grant_number = _reply_value_str(replies.get(_path(fundings_path, funding_item, UUIDs.projectFundingGrantNumberQUuid)))
            funding_status_answer = replies.get(_path(fundings_path, funding_item, UUIDs.projectFundingStatusQUuid), '')
            funding_status = ''
            if funding_status_answer == UUIDs.projectFundingStatusPlannedAUuid:
                funding_status = 'planned'
            elif funding_status_answer == UUIDs.projectFundingStatusAppliedAUuid:
                funding_status = 'applied'
            elif funding_status_answer == UUIDs.projectFundingStatusGrantedAUuid:
                funding_status = 'granted'
            elif funding_status_answer == UUIDs.projectFundingStatusRejectedAUuid:
                funding_status = 'rejected'
            funding = {
                'funder_id': {
                    'identifier': funder_url,
                    'type': 'url',
                },
            }
            if grant_number:
                funding['grant_id'] = {
                    'identifier': grant_number,
                    'type': 'other',
                }
            if funding_status:
                funding['funding_status'] = funding_status
            if funder_url:
                fundings.append(funding)

        project = {
            'title': name,
        }
        if start:
            project['start'] = start
        if end:
            project['end'] = end
        if abstract:
            project['description'] = abstract
        if len(fundings) > 0:
            project['funding'] = fundings
        projects.append(project)
    return projects


def _get_datasets(replies: dict) -> list:
    datasets_path = _path(UUIDs.preservingCUuid, UUIDs.producingQUuid)
    datasets_items = _reply_value_list(replies.get(datasets_path, {}), []) or []
    datasets = []
    for item in datasets_items:
        name = _reply_value_str(replies.get(_path(datasets_path, item, UUIDs.producingNameQUuid)), '(unknown dataset)')
        description = _reply_value_str(replies.get(_path(datasets_path, item, UUIDs.producingDescriptionQUuid)), '')
        personal_answer = replies.get(_path(datasets_path, item, UUIDs.producingPersonalQUuid))
        sensitive_answer = replies.get(_path(datasets_path, item, UUIDs.producingSensitiveQUuid))

        personal_data = 'unknown'
        if personal_answer == UUIDs.producingPersonalYesAUuid:
            personal_data = 'yes'
        elif personal_answer == UUIDs.producingPersonalNoAUuid:
            personal_data = 'no'
        sensitive_data = 'unknown'
        if sensitive_answer == UUIDs.producingSensitiveYesAUuid:
            sensitive_data = 'yes'
        elif sensitive_answer == UUIDs.producingSensitiveNoAUuid:
            sensitive_data = 'no'

        identifiers_path = _path(datasets_path, item, UUIDs.producingIdsQUuid)
        identifiers_items = _reply_value_list(replies.get(identifiers_path, {}), []) or []
        identifiers = []
        for identifier_item in identifiers_items:
            id_type_answer = replies.get(_path(identifiers_path, identifier_item, UUIDs.producingIdsTypeQUuid))
            id_identifier = _reply_value_str(replies.get(_path(identifiers_path, identifier_item, UUIDs.producingIdsIdQUuid)))
            id_type = 'other'
            if id_type_answer == UUIDs.producingIdsTypeHandleAUuid:
                id_type = 'handle'
            elif id_type_answer == UUIDs.producingIdsTypeDoiAUuid:
                id_type = 'doi'
            elif id_type_answer == UUIDs.producingIdsTypeArkAUuid:
                id_type = 'ark'
            elif id_type_answer == UUIDs.producingIdsTypeUrlAUuid:
                id_type = 'url'
            elif id_type_answer == UUIDs.producingIdsTypeOtherAUuid:
                id_type = 'other'
            if id_identifier:
                identifiers.append({
                    'identifier': id_identifier,
                    'type': id_type,
                })

        distributions = []
        published_answer = replies.get(_path(datasets_path, item, UUIDs.publishedQUuid))
        if published_answer == UUIDs.publishedYesAUuid:
            distros_path = _path(datasets_path, item, UUIDs.distrosQUuid)
            distros_items = _reply_value_list(replies.get(distros_path, {}), []) or []
            for distro_item in distros_items:
                access_answer = _reply_value_str(replies.get(_path(distros_path, distro_item, UUIDs.distroAccessQUuid)))
                access = 'closed'
                if access_answer == UUIDs.distroAccessOpenAUuid:
                    access = 'open'
                elif access_answer == UUIDs.distroAccessSharedAUuid:
                    access = 'shared'
                elif access_answer == UUIDs.distroAccessClosedAUuid:
                    access = 'closed'

                licenses_path = _path(distros_path, distro_item, UUIDs.distroLicensesQUuid)
                licenses_items = _reply_value_list(replies.get(licenses_path, {}), []) or []
                licenses = []
                for license_item in licenses_items:
                    license_what_path = _path(licenses_path, license_item, UUIDs.distroLicensesWhatQUuid)
                    license_what_answer = replies.get(license_what_path)
                    if license_what_answer == UUIDs.distroLicensesWhatCC0AUuid:
                        license_ref = 'https://creativecommons.org/publicdomain/zero/1.0/'
                    elif license_what_answer == UUIDs.distroLicensesWhatCCBYAUuid:
                        license_ref = 'https://creativecommons.org/licenses/by/4.0/'
                    elif license_what_answer == UUIDs.distroLicensesWhatOtherAUuid:
                        license_ref = _reply_value_str(replies.get(_path(license_what_path, UUIDs.distroLicensesWhatOtherAUuid, UUIDs.distroLicensesWhatOtherLinkQUuid)))
                    else:
                        license_ref = ''
                    start = _reply_value_str(replies.get(_path(license_what_path, UUIDs.distroLicensesStartQUuid)))
                    if license_ref and start:
                        licenses.append({
                            'license': license_ref,
                            'start_date': start,
                        })

                distribution = {
                    'title': name,
                    'access': access,
                }
                if len(licenses) > 0:
                    distribution['license'] = licenses
                if access:
                    distributions.append(distribution)
        dataset = {
            'dataset_id': {
                'identifier': item,
                'type': 'other',
            },
            'title': name,
            'personal_data': personal_data,
            'sensitive_data': sensitive_data,
        }
        if description:
            dataset['description'] = description
        if len(distributions) > 0:
            dataset['distribution'] = distributions
        if len(identifiers) > 0:
            dataset['identifier'] = identifiers[0]
        datasets.append(dataset)
    return datasets


def _get_costs(replies: dict) -> list:
    projects_path = _path(UUIDs.adminDetailsCUuid, UUIDs.projectsQUuid)
    projects_items = _reply_value_list(replies.get(projects_path, {}), []) or []
    costs = []
    for item in projects_items:
        costs_path = _path(projects_path, item, UUIDs.costQUuid)
        costs_items = _reply_value_list(replies.get(costs_path, {}), []) or []
        for cost_item in costs_items:
            title = _reply_value_str(replies.get(_path(costs_path, cost_item, UUIDs.costTitleQUuid)), '')
            description = _reply_value_str(replies.get(_path(costs_path, cost_item, UUIDs.costDescriptionQUuid)))
            currency_reply = replies.get(_path(costs_path, cost_item, UUIDs.costCurrencyQUuid))
            amount = _reply_value_str(replies.get(_path(costs_path, cost_item, UUIDs.costAmountQUuid)))
            allocation_choices = _reply_value_list(replies.get(_path(costs_path, cost_item, UUIDs.costAllocationQUuid)), [])

            allocations = []
            if isinstance(allocation_choices, list):
                if UUIDs.costAllocationFindabilityAUuid in allocation_choices:
                    allocations.append('findability')
                if UUIDs.costAllocationAccessibilityAUuid in allocation_choices:
                    allocations.append('accessibility')
                if UUIDs.costAllocationInteroperabilityAUuid in allocation_choices:
                    allocations.append('interoperability')
                if UUIDs.costAllocationReusabilityAUuid in allocation_choices:
                    allocations.append('reusability')
                if UUIDs.costManagementAUuid in allocation_choices:
                    allocations.append('cost management')
                allocation_sentence = None
                if len(allocations) > 0:
                    if len(allocations) == 1:
                        allocation_sentence = f'Cost allocation: {allocations[0]}.'
                    else:
                        allocation_sentence = f'Cost allocations: {", ".join(allocations[:-1])} and {allocations[-1]}.'

            cost = {
                'title': title,
            }
            if amount is not None:
                cost['amount'] = float(amount) if amount else None
            if description or allocation_sentence:
                cost['description'] = f'{allocation_sentence} {description}'.strip()
            if currency_reply:
                cost['currency'] = _reply_currency(currency_reply)
            costs.append(cost)
    return costs


def map_dsw_root_to_madmp(client_url: str, project_data: dict) -> dict:
    replies = project_data.get('replies', {})
    project_uuid = project_data.get('uuid')

    contributors, contacts = _get_contributors(replies)
    projects = _get_projects(replies)
    datasets = _get_datasets(replies)
    costs = _get_costs(replies)
    contact = None
    if len(contacts) > 0:
        contact = {
            'contact_id': contacts[0]['contributor_id'],
            'mbox': contacts[0]['mbox'],
            'name': contacts[0]['name'],
        }
    ethical_issues_exist, ethical_issues_description = _get_ethical_issues(replies)
    dmp_description = (f'This maDMP has been created using {client_url} (as a living document);'
                       f'this specific snapshot is intended for maDMP evaluation purposes.')

    return {
        'title': project_data.get('name'),
        'description': dmp_description,
        'language': 'eng',
        'dmp_id': {
            'identifier': f'{client_url}/projects/{project_uuid}',
            'type': 'url',
        },
        'contact': contact,
        'contributor': contributors,
        'project': projects,
        'ethical_issues_exist': ethical_issues_exist,
        'ethical_issues_description': ethical_issues_description,
        'dataset': datasets,
        'cost': costs,
        'created': '',
        'modified': '',
    }
