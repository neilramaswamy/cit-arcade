export enum ControlButton {
    Up = 1,
    Down,
    Left,
    Right,

    Pause,
    Select
}

interface AuthedRequest {
    authToken: string;
}

export interface PostUserPasswordRequest extends AuthedRequest {}
export interface PostUserPasswordResponse {
    playerIndex: number;
}

export interface PostUserSendControlRequest extends AuthedRequest {
    button: ControlButton;
}

export interface PostUserSendControlResponse {}

// -----------------
// ADMIN ROUTES
// -----------------
export interface PostAdminGetPasswordsRequest extends AuthedRequest {}

export interface PostAdminGetPasswordsResponse {
    authTokens: [];
}

export interface PostAdminRotatePasswordsRequest extends AuthedRequest {}
export interface PostAdminRotatePasswordsResponse {
    authTokens: [];
}
