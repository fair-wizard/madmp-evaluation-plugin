import pytest

from madmp_evaluation_plugin_service.mapping import UUIDs as U  # noqa: N814
from madmp_evaluation_plugin_service.mapping import markdown_plain, to_madmp

CLIENT_URL = 'https://wizard.example.com'
CREATED = '2026-01-01T10:00:00Z'
MODIFIED = '2026-02-01T10:00:00Z'


def p(*parts: str) -> str:
    return '.'.join(parts)


def answer(uuid: str) -> dict:
    return {'value': {'type': 'AnswerReply', 'value': uuid}, 'createdAt': '2026-01-15T10:00:00Z'}


def string(value: str) -> dict:
    return {'value': {'type': 'StringReply', 'value': value}, 'createdAt': '2026-01-15T10:00:00Z'}


def items(*values: str) -> dict:
    return {'value': {'type': 'ItemListReply', 'value': list(values)}, 'createdAt': '2026-01-15T10:00:00Z'}


def choices(*values: str) -> dict:
    return {'value': {'type': 'MultiChoiceReply', 'value': list(values)}, 'createdAt': '2026-01-15T10:00:00Z'}


def integration(value: str, raw: dict | None = None) -> dict:
    if raw is None:
        reply = {'type': 'PlainType', 'value': value}
    else:
        reply = {'type': 'IntegrationType', 'value': value, 'raw': raw}
    return {'value': {'type': 'IntegrationReply', 'value': reply}, 'createdAt': '2026-01-15T10:00:00Z'}


CONTRIBUTORS = p(U.adminDetailsCUuid, U.contributorsQUuid)
PROJECTS = p(U.adminDetailsCUuid, U.projectsQUuid)
DATASETS = p(U.preservingCUuid, U.producingQUuid)
NREF = p(U.reusingCUuid, U.preexistingQUuid, U.preexistingYesAUuid, U.nrefDataQUuid)
NREF_USED = p(NREF, 'n1', U.nrefDataUseQUuid, U.nrefDataUseYesAUuid)
NREF_LEGAL = p(NREF_USED, U.nrefDataPersonalQUuid, U.nrefDataPersonalYesAUuid, U.nrefDataPersonalLegalBasisQUuid)
GDPR = p(U.creatingCUuid, U.collectPersonalQUuid, U.collectPersonalYesAUuid, U.cpersGdprQUuid, U.cpersGdprExploreAUuid)
LEGISLATION = p(U.creatingCUuid, U.ethicsLegislationQUuid, U.ethicsLegislationYesAUuid)
PRIVACY = p(U.givingAccessCUuid, U.canOpenQUuid, U.canOpenNoAUuid, U.legalReasonsQUuid, U.legalReasonsYesAUuid,
            U.privacyReasonsQUuid, U.privacyReasonsYesAUuid)
DISTROS = p(DATASETS, 'd1', U.publishedQUuid, U.publishedYesAUuid, U.distrosQUuid)
FUNDINGS = p(PROJECTS, 'p1', U.projectFundingQUuid)
COSTS = p(PROJECTS, 'p1', U.costQUuid)

REPLIES = {
    # Contributors
    CONTRIBUTORS: items('c1', 'c2', 'c3'),
    p(CONTRIBUTORS, 'c1', U.contributorNameQUuid): string('Alice Doe'),
    p(CONTRIBUTORS, 'c1', U.contributorEmailQUuid): string('alice@example.com'),
    p(CONTRIBUTORS, 'c1', U.contributorOrcidQUuid): integration(
        '**Alice** **Doe** \nORCID: [**0000-0002-1825-0097**](https://orcid.org/0000-0002-1825-0097)',
        {'orcid-id': '0000-0002-1825-0097'},
    ),
    p(CONTRIBUTORS, 'c1', U.contributorRoleQUuid): choices(U.contributorRoleDataManagerAUuid, U.contributorRoleContactPersonAUuid),
    p(CONTRIBUTORS, 'c2', U.contributorNameQUuid): string('Bob Roe'),
    p(CONTRIBUTORS, 'c2', U.contributorRoleQUuid): choices(U.contributorRoleSupervisorAUuid),
    p(CONTRIBUTORS, 'c3', U.contributorNameQUuid): string('No Role'),
    # Projects, funding and costs
    PROJECTS: items('p1', 'p2'),
    p(PROJECTS, 'p1', U.projectNameQUuid): string('Great Project'),
    p(PROJECTS, 'p1', U.projectAbstractQUuid): string('Some **bold** [text](https://example.com).'),
    p(PROJECTS, 'p1', U.projectStartQUuid): string('2026-01-01'),
    p(PROJECTS, 'p1', U.projectEndQUuid): string('2028-12-31'),
    FUNDINGS: items('f1', 'f2'),
    p(FUNDINGS, 'f1', U.projectFundingFunderQUuid): integration(
        '[**European Commission**](http://dx.doi.org/10.13039/501100000780) (Belgium)',
        {'uri': 'http://dx.doi.org/10.13039/501100000780', 'name': 'European Commission'},
    ),
    p(FUNDINGS, 'f1', U.projectFundingStatusQUuid): answer(U.projectFundingStatusGrantedAUuid),
    p(FUNDINGS, 'f1', U.projectFundingGrantNumberQUuid): string('101000000'),
    p(FUNDINGS, 'f2', U.projectFundingFunderQUuid): integration('My local funder'),
    COSTS: items('k1', 'k2'),
    p(COSTS, 'k1', U.costTitleQUuid): string('Storage'),
    p(COSTS, 'k1', U.costDescriptionQUuid): string('Long-term storage'),
    p(COSTS, 'k1', U.costAmountQUuid): string('1 000,50'),
    p(COSTS, 'k1', U.costCurrencyQUuid): integration('Euro, EUR', {'code': 'EUR', 'name': 'Euro'}),
    p(COSTS, 'k1', U.costAllocationQUuid): choices(U.costAllocationFindabilityAUuid, U.costAllocationAccessibilityAUuid, U.costManagementAUuid),
    p(COSTS, 'k2', U.costTitleQUuid): string('Unclear'),
    p(COSTS, 'k2', U.costAmountQUuid): string('a lot'),
    p(COSTS, 'k2', U.costCurrencyQUuid): integration('some money'),
    # Datasets
    DATASETS: items('d1', 'd2'),
    p(DATASETS, 'd1', U.producingNameQUuid): string('Survey'),
    p(DATASETS, 'd1', U.producingDescriptionQUuid): string('Survey _answers_'),
    p(DATASETS, 'd1', U.producingPersonalQUuid): answer(U.producingPersonalYesAUuid),
    p(DATASETS, 'd1', U.producingSensitiveQUuid): answer(U.producingSensitiveNoAUuid),
    p(DATASETS, 'd1', U.producingTypeQUuid): answer(U.producingTypeRawAUuid),
    p(DATASETS, 'd1', U.producingIdsQUuid): items('i1'),
    p(DATASETS, 'd1', U.producingIdsQUuid, 'i1', U.producingIdsTypeQUuid): answer(U.producingIdsTypeDoiAUuid),
    p(DATASETS, 'd1', U.producingIdsQUuid, 'i1', U.producingIdsIdQUuid): string('10.1234/survey'),
    p(DATASETS, 'd1', U.keptQUuid): answer(U.keptFixedPeriodAUuid),
    p(DATASETS, 'd1', U.keptQUuid, U.keptFixedPeriodAUuid, U.keptFixedPeriodHowLongQUuid): string('10 years'),
    p(DATASETS, 'd1', U.keptMetadataQUuid): answer(U.keptMetadataYesAUuid),
    p(DATASETS, 'd1', U.publishedQUuid): answer(U.publishedYesAUuid),
    DISTROS: items('r1', 'r2'),
    p(DISTROS, 'r1', U.distroAccessQUuid): answer(U.distroAccessOpenAUuid),
    p(DISTROS, 'r1', U.distroRepositoryQUuid): answer(U.distroRepositoryGeneralAUuid),
    p(DISTROS, 'r1', U.distroRepositoryQUuid, U.distroRepositoryGeneralAUuid, U.distroRepositoryGeneralWhichQUuid): integration(
        '[**Zenodo**](https://fairsharing.org/2521)', {'id': 2521, 'name': 'Zenodo', 'homepage': 'https://zenodo.org'},
    ),
    p(DISTROS, 'r1', U.distroLicensesQUuid): items('l1', 'l2'),
    p(DISTROS, 'r1', U.distroLicensesQUuid, 'l1', U.distroLicensesWhatQUuid): answer(U.distroLicensesWhatCCBYAUuid),
    p(DISTROS, 'r1', U.distroLicensesQUuid, 'l1', U.distroLicensesStartQUuid): string('2027-01-01'),
    p(DISTROS, 'r1', U.distroLicensesQUuid, 'l2', U.distroLicensesWhatQUuid): answer(U.distroLicensesWhatOtherAUuid),
    p(DISTROS, 'r1', U.distroLicensesQUuid, 'l2', U.distroLicensesWhatQUuid, U.distroLicensesWhatOtherAUuid,
      U.distroLicensesWhatOtherLinkQUuid): string('https://example.com/license'),
    p(DISTROS, 'r1', U.distroLicensesQUuid, 'l2', U.distroLicensesStartQUuid): string('2027-06-01'),
    p(DISTROS, 'r2', U.distroRepositoryQUuid): answer(U.distroRepositoryInstitutionalAUuid),
    p(DATASETS, 'd2', U.producingNameQUuid): string(''),
    p(DATASETS, 'd2', U.producingIdsQUuid): items('i2'),
    p(DATASETS, 'd2', U.producingIdsQUuid, 'i2', U.producingIdsTypeQUuid): answer(U.producingIdsTypeNoneAUuid),
    p(DATASETS, 'd2', U.producingIdsQUuid, 'i2', U.producingIdsIdQUuid): string('none'),
    # Stale reply under an unselected answer must be ignored
    p(DATASETS, 'd2', U.publishedQUuid, U.publishedYesAUuid, U.distrosQUuid): items('r3'),
    # Ethical issues
    p(U.reusingCUuid, U.preexistingQUuid): answer(U.preexistingYesAUuid),
    NREF: items('n1'),
    p(NREF, 'n1', U.nrefDataNameQUuid): string('Census'),
    p(NREF, 'n1', U.nrefDataWhereQUuid): string('https://census.example.com'),
    p(NREF, 'n1', U.nrefDataUseQUuid): answer(U.nrefDataUseYesAUuid),
    p(NREF_USED, U.nrefDataPersonalQUuid): answer(U.nrefDataPersonalYesAUuid),
    NREF_LEGAL: answer(U.nrefDataPersonalLegalBasisOtherAUuid),
    p(NREF_LEGAL, U.nrefDataPersonalLegalBasisOtherAUuid, U.nrefDataPersonalLegalBasisOtherQUuid): answer(U.nrefDataPersonalLegalBasisVitInterAUuid),
    p(NREF_USED, U.nrefDataEthicalAppQUuid): answer(U.nrefDataEthicalAppNewAUuid),
    p(U.creatingCUuid, U.collectPersonalQUuid): answer(U.collectPersonalYesAUuid),
    p(U.creatingCUuid, U.collectPersonalQUuid, U.collectPersonalYesAUuid, U.cpersGdprQUuid): answer(U.cpersGdprExploreAUuid),
    p(GDPR, U.cpersLegalBasisQUuid): answer(U.cpersLegalBasisOtherAUuid),
    p(GDPR, U.cpersLegalBasisQUuid, U.cpersLegalBasisOtherAUuid, U.cpersLegalBasisOtherQUuid): answer(U.cpersLegalBasisLegitAUuid),
    p(GDPR, U.cpersNeedDpiaQUuid): answer(U.cpersNeedDpiaYesAUuid),
    p(U.creatingCUuid, U.ethicsLegislationQUuid): answer(U.ethicsLegislationYesAUuid),
    p(LEGISLATION, U.ethicsReviewQUuid): answer(U.ethicsReviewYesAUuid),
    p(LEGISLATION, U.ethicsHumanSubjectsQUuid): answer(U.ethicsHumanSubjectsYesAUuid),
    p(U.givingAccessCUuid, U.canOpenQUuid): answer(U.canOpenNoAUuid),
    p(U.givingAccessCUuid, U.canOpenQUuid, U.canOpenNoAUuid, U.legalReasonsQUuid): answer(U.legalReasonsYesAUuid),
    p(U.givingAccessCUuid, U.canOpenQUuid, U.canOpenNoAUuid, U.legalReasonsQUuid, U.legalReasonsYesAUuid,
      U.privacyReasonsQUuid): answer(U.privacyReasonsYesAUuid),
    p(PRIVACY, U.privacyRestrictionsQUuid): answer(U.privacyRestrictionsYesEUAUuid),
    p(PRIVACY, U.privacyAnonQUuid): answer(U.privacyAnonYesAUuid),
}

PACKAGE = {
    'organizationId': 'dsw',
    'kmId': 'root',
    'version': '2.7.0',
    'name': 'Common DSW Knowledge Model',
}


def project(replies: dict, package: dict | None = None) -> dict:
    return {
        'uuid': 'b0f5c1b8-2b6a-4a36-a3b1-5d7a4c52c1f0',
        'name': 'My DMP',
        'knowledgeModelPackage': package or PACKAGE,
        'replies': replies,
    }


@pytest.fixture(name='dmp')
def fixture_dmp() -> dict:
    return to_madmp(project(REPLIES), CLIENT_URL, CREATED, MODIFIED)['dmp']


def test_root(dmp: dict) -> None:
    assert dmp['title'] == 'My DMP'
    assert dmp['created'] == CREATED
    assert dmp['modified'] == MODIFIED
    assert dmp['language'] == 'eng'
    assert dmp['dmp_id'] == {'identifier': f'{CLIENT_URL}/projects/b0f5c1b8-2b6a-4a36-a3b1-5d7a4c52c1f0', 'type': 'url'}
    assert 'dsw:root:2.7.0' in dmp['description']


def test_contributors_and_contact(dmp: dict) -> None:
    alice_id = {'identifier': 'https://orcid.org/0000-0002-1825-0097', 'type': 'orcid'}
    assert dmp['contributor'] == [
        {'contributor_id': alice_id, 'name': 'Alice Doe', 'role': ['contact person', 'data manager'], 'mbox': 'alice@example.com'},
        {'contributor_id': {'identifier': 'c2', 'type': 'other'}, 'name': 'Bob Roe', 'role': ['supervisor']},
    ]
    assert dmp['contact'] == {'contact_id': alice_id, 'mbox': 'alice@example.com', 'name': 'Alice Doe'}


def test_projects(dmp: dict) -> None:
    assert dmp['project'] == [{
        'title': 'Great Project',
        'description': 'Some bold text.',
        'start': '2026-01-01',
        'end': '2028-12-31',
        'funding': [
            {
                'funder_id': {'identifier': 'http://dx.doi.org/10.13039/501100000780', 'type': 'fundref'},
                'funding_status': 'granted',
                'grant_id': {'identifier': '101000000', 'type': 'other'},
            },
            {'funder_id': {'identifier': 'My local funder', 'type': 'other'}},
        ],
    }]


def test_costs(dmp: dict) -> None:
    assert dmp['cost'] == [
        {
            'title': 'Storage',
            'description': ('Long-term storage. This resource is allocated for ensuring findability, '
                            'ensuring accessibility, and supporting management of data.'),
            'value': 1000.5,
            'currency_code': 'EUR',
        },
        {'title': 'Unclear'},
    ]


def test_datasets(dmp: dict) -> None:
    survey, unnamed = dmp['dataset']
    assert survey == {
        'dataset_id': {'identifier': '10.1234/survey', 'type': 'doi'},
        'title': 'Survey',
        'description': 'Survey answers',
        'personal_data': 'yes',
        'sensitive_data': 'no',
        'type': 'raw data',
        'preservation_statement': ('The data set will be kept for a fixed period (10 years). '
                                   'The metadata will be available even when the data no longer exists.'),
        'distribution': [{
            'title': 'Survey',
            'data_access': 'open',
            'description': 'Distributed via a general-purpose repository (Zenodo).',
            'host': {'title': 'Zenodo', 'url': 'https://zenodo.org'},
            'license': [
                {'license_ref': 'https://creativecommons.org/licenses/by/4.0/', 'start_date': '2027-01-01'},
                {'license_ref': 'https://example.com/license', 'start_date': '2027-06-01'},
            ],
        }],
    }
    assert unnamed == {
        'dataset_id': {'identifier': 'd2', 'type': 'other'},
        'title': '(unnamed dataset)',
        'personal_data': 'unknown',
        'sensitive_data': 'unknown',
    }


def test_ethical_issues(dmp: dict) -> None:
    assert dmp['ethical_issues_exist'] == 'yes'
    assert dmp['ethical_issues_description'] == ' '.join([
        'Non-reference dataset "Census" (https://census.example.com) contains personal data based on vital interests.',
        'Non-reference dataset "Census" (https://census.example.com) has been ethically approved but new ethical approval '
        'under research ethics laws will be required to cover our intended use of the data.',
        'We will collect data connected to a person, i.e. "personal data".',
        'We have a legitimate interest: data subjects all expect us to do this data processing because of who we are.',
        'We need to conduct a data protection impact assessment (DPIA).',
        'The data collection is subject to ethical legislation.',
        'The data collection is covered by an ethical review.',
        'The data collection involves human subjects.',
        'There are legal reasons why some of our data cannot be open.',
        'There are privacy reasons why some of our data cannot be open.',
        'Our data must stay in EU.',
        'We can make the data more openly available by anonymization.',
    ])


def test_ethical_issues_no_and_unknown() -> None:
    no_issues = {
        p(U.creatingCUuid, U.collectPersonalQUuid): answer(U.collectPersonalNoAUuid),
        p(U.creatingCUuid, U.ethicsLegislationQUuid): answer(U.ethicsLegislationNoAUuid),
    }
    dmp = to_madmp(project(no_issues), CLIENT_URL, CREATED, MODIFIED)['dmp']
    assert dmp['ethical_issues_exist'] == 'no'
    assert 'ethical_issues_description' not in dmp
    dmp = to_madmp(project({}), CLIENT_URL, CREATED, MODIFIED)['dmp']
    assert dmp['ethical_issues_exist'] == 'unknown'


def test_empty_project() -> None:
    dmp = to_madmp(project({}), CLIENT_URL, CREATED, MODIFIED)['dmp']
    assert dmp['dataset'] == []
    for key in ('contact', 'contributor', 'project', 'cost'):
        assert key not in dmp


def test_contact_fallback() -> None:
    replies = {
        CONTRIBUTORS: items('c1'),
        p(CONTRIBUTORS, 'c1', U.contributorNameQUuid): string('Carol'),
        p(CONTRIBUTORS, 'c1', U.contributorEmailQUuid): string('carol@example.com'),
        p(CONTRIBUTORS, 'c1', U.contributorOrcidQUuid): integration('Carol, ORCID: 0000-0001-5109-3700'),
        p(CONTRIBUTORS, 'c1', U.contributorRoleQUuid): choices(U.contributorRoleResearcherAUuid),
    }
    dmp = to_madmp(project(replies), CLIENT_URL, CREATED, MODIFIED)['dmp']
    assert dmp['contact'] == {
        'contact_id': {'identifier': 'https://orcid.org/0000-0001-5109-3700', 'type': 'orcid'},
        'mbox': 'carol@example.com',
        'name': 'Carol',
    }


def test_lifesciences_supported() -> None:
    package = {**PACKAGE, 'kmId': 'lifesciences'}
    assert to_madmp(project({}, package), CLIENT_URL, CREATED, MODIFIED)['dmp']['title'] == 'My DMP'


def test_unsupported_km() -> None:
    with pytest.raises(ValueError, match='Unsupported knowledge model package'):
        to_madmp(project({}, {**PACKAGE, 'organizationId': 'other'}), CLIENT_URL, CREATED, MODIFIED)


@pytest.mark.parametrize(('text', 'expected'), [
    ('**bold** and _italic_ in snake_case_name', 'bold and italic in snake_case_name'),
    ('# Heading\n\n- item [link](https://example.com)\n- `code`', 'Heading item link code'),
    ('![img](data:image/png;base64,xyz) text', 'text'),
])
def test_markdown_plain(text: str, expected: str) -> None:
    assert markdown_plain(text) == expected
