from typing import ClassVar

from pulpcore.cli.common.context import (
    EntityDefinition,
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)
from pulpcore.cli.common.generic import PluginRequiredVersion as PRV


class PulpPythonContentContext(PulpEntityContext):
    ENTITY = "python content"
    ENTITIES = "python content"
    HREF = "python_python_package_content_href"
    LIST_ID = "content_python_packages_list"
    READ_ID = "content_python_packages_read"
    CREATE_ID = "content_python_packages_create"


class PulpPythonDistributionContext(PulpEntityContext):
    ENTITY = "python distribution"
    ENTITIES = "python distributions"
    HREF = "python_python_distribution_href"
    LIST_ID = "distributions_python_pypi_list"
    READ_ID = "distributions_python_pypi_read"
    CREATE_ID = "distributions_python_pypi_create"
    UPDATE_ID = "distributions_python_pypi_partial_update"
    DELETE_ID = "distributions_python_pypi_delete"
    NULLABLES = {"publication"}


class PulpPythonPublicationContext(PulpEntityContext):
    ENTITY = "python publication"
    ENTITIES = "python publications"
    HREF = "python_python_publication_href"
    LIST_ID = "publications_python_pypi_list"
    READ_ID = "publications_python_pypi_read"
    CREATE_ID = "publications_python_pypi_create"
    DELETE_ID = "publications_python_pypi_delete"

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpPythonRemoteContext(PulpRemoteContext):
    ENTITY = "python remote"
    ENTITIES = "python remotes"
    HREF = "python_python_remote_href"
    LIST_ID = "remotes_python_python_list"
    CREATE_ID = "remotes_python_python_create"
    BANDERSNATCH_ID: ClassVar[str] = "remotes_python_python_from_bandersnatch"
    UPDATE_ID = "remotes_python_python_partial_update"
    DELETE_ID = "remotes_python_python_delete"
    field_versions = {
        "keep_latest_packages": [PRV("python", "3.2.0")],
        "exclude_platforms": [PRV("python", "3.2.0")],
        "package_types": [PRV("python", "3.2.0")],
    }

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        for field in body.keys():
            if field in self.field_versions:
                for item in self.field_versions[field]:
                    self.pulp_ctx.needs_plugin(*item)
        return body


class PulpPythonRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "python_python_repository_version_href"
    REPOSITORY_HREF = "python_python_repository_href"
    LIST_ID = "repositories_python_python_versions_list"
    READ_ID = "repositories_python_python_versions_read"
    DELETE_ID = "repositories_python_python_versions_delete"
    REPAIR_ID = "repositories_python_python_versions_repair"


class PulpPythonRepositoryContext(PulpRepositoryContext):
    HREF = "python_python_repository_href"
    LIST_ID = "repositories_python_python_list"
    READ_ID = "repositories_python_python_read"
    CREATE_ID = "repositories_python_python_create"
    UPDATE_ID = "repositories_python_python_partial_update"
    DELETE_ID = "repositories_python_python_delete"
    SYNC_ID = "repositories_python_python_sync"
    MODIFY_ID = "repositories_python_python_modify"
    VERSION_CONTEXT = PulpPythonRepositoryVersionContext