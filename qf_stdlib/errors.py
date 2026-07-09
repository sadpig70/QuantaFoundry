"""Fail-closed exceptions for the QF stdlib lookup layer."""


class QFStdlibError(Exception):
    """Base error for qf_stdlib."""


class ValidationError(QFStdlibError):
    """A proof-bearing sidecar is inconsistent with the live registry."""


class NotFoundError(QFStdlibError):
    """A lookup target is not in the canonical stdlib surface."""


class UnsupportedAdapter(QFStdlibError):
    """Circuit framework adapter is not available or not yet supported."""


class AdapterConventionError(QFStdlibError):
    """A circuit adapter input does not satisfy the pinned convention."""
