import { FlashError } from './FlashError'

export function ErrorMessage({ message }: { message: string | null }) {
    return (
        <div className="Projects__Detail__Content">
            <div className="col col-detail mx-auto">
                <FlashError message={message ?? 'An unknown error occurred'} />
            </div>
        </div>
    )
}
